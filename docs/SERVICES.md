# 서비스와 함수 정의

정확한 타입은 코드(`backend/src/auction_lens/`)가 기준이다. 이 문서는 서비스별 책임과 함수의 입출력, 적용 규칙을 설명한다.

## 한눈에 보기

| 서비스 | 모듈 | 책임 | 사용하는 포트 |
|---|---|---|---|
| ListingSearchService | `services/listing_search.py` | 경매·공매 물건 검색, 정규화, 저장 | ListingSource, ListingRepository |
| DocumentCollectionService | `services/document_collection.py` | 문서 다운로드·업로드, 파싱, 권리분석 입력 생성 | ListingSource, DocumentParser, DocumentStore |
| 권리분석 | `services/rights_analysis.py` | 말소기준권리, 인수·소멸, 임차인, 배당, 위험 플래그 | 없음 (순수 함수) |
| MarketComparisonService | `services/market_comparison.py` | 비교 거래·호가 수집, 시세 추정 | TradeDataSource, AskingPriceSource |
| TransitProximityService | `services/transit_proximity.py` | 좌표 변환, 지하철역 거리, 역세권 등급 | Geocoder, StationFinder, WalkingRouter |
| 수익성 | `services/profitability.py` | 취득 비용, 세금, 시나리오, 입찰 상한가 | 없음 (순수 함수) |
| ReportService | `services/report.py` | 종합 리포트, 점수, 순위 | AnalysisRepository |
| AnalysisPipeline | `pipeline.py` | 위 단계를 순서대로 실행 | 서비스 전체 |

## 1. ListingSearchService — 물건 검색

| 함수 | 입력 | 출력 | 설명 |
|---|---|---|---|
| `search(criteria)` | SearchCriteria | list[Listing] | 소스별로 검색해 공통 모델로 정규화하고, 중복을 제거해 저장 |
| `get(listing_id)` | 물건 ID | Listing | 저장된 물건 조회 |
| `refresh(listing_id)` | 물건 ID | Listing | 상세 재수집. 기일 변경, 유찰, 취하 반영 |

검색 조건: 매각 유형(경매/공매), 지역(법정동 코드), 물건 종류, 최저가 범위, 최소 유찰 횟수, 입찰 기일 범위.

## 2. DocumentCollectionService — 자료 수집과 파싱

| 함수 | 입력 | 출력 | 설명 |
|---|---|---|---|
| `collect(listing)` | Listing | list[Document] | 소스의 문서 목록을 받아 다운로드하고 해시로 중복을 걸러 저장 |
| `register_upload(listing_id, doc_type, filename, content)` | 파일 | Document | 사용자가 올린 문서(등기사항증명서 등) 등록 |
| `parse(document)` | Document | ParsedDocument | 문서 종류별로 텍스트와 구조화 필드 추출 |
| `build_rights_input(listing_id)` | 물건 ID | RightsInput | 파싱 결과를 합쳐 등기 권리, 임차인, 특이사항 목록 생성 |

수집 대상 문서:

| 문서 | 얻는 정보 |
|---|---|
| 매각물건명세서 | 최선순위 설정일, 임차인(전입일·확정일자·보증금·배당요구), 인수되는 권리, 비고 |
| 현황조사서 | 점유 관계, 임대차 현황 |
| 감정평가서 | 감정가 내역, 면적, 위치·상태 |
| 등기사항증명서 (업로드) | 갑구·을구 권리 전체와 순위 |
| 건축물대장 | 용도, 위반건축물 여부 |
| 공매 재산명세·공고 | 공매 물건의 권리·임대차·유의사항 |

## 3. 권리분석

| 함수 | 입력 | 출력 | 설명 |
|---|---|---|---|
| `find_baseline_right(rights)` | 등기 권리 목록 | RegistryRight 또는 None | 말소기준권리 판정 |
| `judge_rights(rights, baseline)` | 권리 목록, 말소기준권리 | list[RightJudgement] | 권리별 인수·소멸 판정과 근거 |
| `judge_tenants(tenants, baseline)` | 임차인 목록, 말소기준권리 | list[TenantJudgement] | 대항력, 우선변제권 판정 |
| `simulate_distribution(sale_price, rights, tenants, ...)` | 예상 낙찰가 등 | list[DistributionEntry] | 배당 순위별 배당액 계산 |
| `detect_risk_flags(listing, rights_input)` | 물건, 권리분석 입력 | list[RiskFlag] | 특수 권리·주의 사항 표시 |
| `analyze(listing, rights_input, expected_sale_price)` | 위 전체 | RightsAnalysis | 종합 실행. 인수금액 합계와 요약 생성 |

적용 규칙:

- **말소기준권리**: (근)저당권, (가)압류, 담보가등기, 경매개시결정등기, 그리고 배당요구를 했거나 경매를 신청한 선순위 전세권 중 가장 먼저 등기된 것.
- **인수·소멸**: 말소기준권리보다 늦은 권리는 소멸, 빠른 권리는 인수. 유치권, 법정지상권, 분묘기지권 등은 순위와 무관하게 인수될 수 있어 위험 플래그로 따로 표시한다.
- **임차인 대항력**: 전입신고 다음 날 0시 기준으로 말소기준권리보다 빠르면 대항력이 있고, 배당받지 못한 보증금은 낙찰자가 인수한다.
- **우선변제**: 대항요건과 확정일자를 갖추고 배당요구 종기까지 배당요구를 한 경우. 소액임차인 최우선변제는 지역과 담보물권 설정일에 따른 기준표(`rules/`)를 적용한다.
- **배당 순서**: 집행비용 → 소액임차인 최우선변제·임금채권 → 당해세 → 확정일자 임차인·담보물권·조세(일자순) → 일반채권.
- **공매**: 인도명령 제도가 없어 명도 비용·기간을 더 크게 잡는다.

판정할 수 없는 항목은 추정하지 않고 `UNCERTAIN`으로 두어 사람이 확인하게 한다.

## 4. MarketComparisonService — 시세 비교

| 함수 | 입력 | 출력 | 설명 |
|---|---|---|---|
| `fetch_comparables(listing, months, area_tolerance)` | 물건, 기간, 면적 허용 오차 | list[TradeRecord] | 같은 법정동·같은 종류·비슷한 면적의 실거래 조회 |
| `fetch_asking_listings(listing)` | 물건 | list[AskingListing] | 현재 매물 호가 조회 (소스가 있을 때) |
| `estimate_market_price(listing, comparables)` | 물건, 비교 거래 | int 또는 None | 같은 단지 우선, 최근 거래 가중으로 시세 추정 |
| `compare(listing)` | 물건 | MarketComparison | 추정 시세, ㎡당 가격, 최저가/시세 비율, 전세가율 |

비교 대상 선정 순서: 같은 단지·같은 면적 → 같은 단지 유사 면적 → 같은 법정동 유사 물건. 표본이 적으면 기간을 넓히고 표본 수를 결과에 남긴다.

## 5. TransitProximityService — 역세권 분석

| 함수 | 입력 | 출력 | 설명 |
|---|---|---|---|
| `locate(listing)` | 물건 | Coordinate 또는 None | 주소를 좌표로 변환 |
| `nearest_stations(coordinate, radius_m, limit)` | 좌표 | list[StationDistance] | 반경 내 지하철역과 직선·도보 거리 |
| `grade(nearest)` | 가장 가까운 역 | TransitGrade | 500m 이내 역세권, 1km 이내 준역세권, 그 밖 비역세권 |
| `analyze(listing)` | 물건 | TransitProximity | 종합 실행 |

도보 경로 API를 쓸 수 없으면 직선거리 × 1.3을 도보 거리로, 분당 80m로 시간을 추정하고 추정값임을 표시한다.

## 6. 수익성 분석

| 함수 | 입력 | 출력 | 설명 |
|---|---|---|---|
| `calc_acquisition_tax(price, property_type, ...)` | 낙찰가, 종류, 보유 주택 수, 면적 | int | 취득세와 부가세(지방교육세·농어촌특별세) |
| `calc_acquisition_cost(listing, assumptions, assumed_amount)` | 물건, 가정, 인수금액 | AcquisitionCost | 낙찰가 + 세금 + 법무비 + 인수금액 + 명도비 + 수리비 + 체납 관리비 |
| `calc_capital_gains_tax(gain, holding_months, property_type)` | 양도차익, 보유 기간 | int | 보유 기간별 양도소득세 |
| `simulate(listing, assumptions, assumed_amount)` | 물건, 가정 | ProfitScenario | 한 가지 가정에 대한 순이익, 수익률, 임대수익률 |
| `build_scenarios(listing, rights, market, base)` | 권리분석, 시세 비교 | ProfitAnalysis | 보수·기준·낙관 시나리오 |
| `solve_max_bid(listing, target_roi, ...)` | 목표 수익률 | int | 목표 수익률을 만족하는 입찰 상한가 |

세율과 기준은 `rules/` 데이터에서 읽고, 결과에 적용 기준일을 남긴다.

## 7. ReportService — 리포트

| 함수 | 입력 | 출력 | 설명 |
|---|---|---|---|
| `score(rights, market, transit, profit)` | 분석 결과 | int (0~100) | 권리 안전성, 가격 매력, 입지, 수익률을 합친 점수 |
| `build(listing_id)` | 물건 ID | ListingReport | 저장된 분석 결과를 모아 리포트 구성 |
| `rank(reports)` | 리포트 목록 | list[ListingReport] | 점수순 정렬. 인수 위험이 큰 물건은 뒤로 |

## 8. AnalysisPipeline

| 함수 | 입력 | 출력 | 설명 |
|---|---|---|---|
| `run(listing_id, assumptions)` | 물건 ID, 수익 가정 | ListingReport | 수집 → 파싱 → 권리 → 시세 → 역세권 → 수익성 → 리포트 |
| `run_search(criteria, assumptions)` | 검색 조건 | list[ListingReport] | 검색 결과 전체를 분석하고 순위를 매김 |

한 단계가 실패해도 나머지는 계속 진행하고, 리포트에 빠진 단계와 사유를 기록한다.

## 9. 인터페이스 (예정)

CLI (Phase 1~):

```
auction-lens search --region 11680 --type apartment --max-price 900000000
auction-lens analyze <listing_id> --bid 650000000
auction-lens report <listing_id>
```

REST API (Phase 6~):

| 메서드 | 경로 | 설명 |
|---|---|---|
| POST | `/searches` | 조건으로 검색 실행 |
| GET | `/listings` | 저장된 물건 목록 |
| GET | `/listings/{id}` | 물건 상세 |
| POST | `/listings/{id}/documents` | 문서 업로드 |
| POST | `/listings/{id}/analyze` | 분석 파이프라인 실행 |
| GET | `/listings/{id}/report` | 종합 리포트 |
