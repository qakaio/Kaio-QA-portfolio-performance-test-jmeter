# JMeter Performance Testing Portfolio

![JMeter Tests](https://github.com/qakaio/Kaio-QA-portfolio-performance-test-jmeter/actions/workflows/jmeter.yml/badge.svg)
![Allure Report](https://img.shields.io/badge/Allure-Report-brightgreen?logo=allure)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Performance testing scripts and reports using **Apache JMeter** to evaluate API and web application responsiveness, stability, and scalability under load.

Built by [Kaio Garcia](https://github.com/qakaio) — Senior QA Engineer

---

## Project Overview

| Aspect | Details |
|--------|---------|
| **Tool** | Apache JMeter 5.6+ |
| **Test Format** | JMX (XML-based test plans) |
| **Target Types** | REST APIs, Web Applications |
| **Reporting** | HTML Dashboard, CSV, JTL + **Allure Report** |
| **CI/CD** | GitHub Actions, Jenkins compatible |

---

## Test Plans Included

| Test Plan | Purpose | Virtual Users | Duration |
|-----------|---------|---------------|----------|
| **Load Test** | Baseline performance | 10 | 60s |
| **Stress Test** | Breaking point | 50-100 | 120s |
| **Spike Test** | Sudden load increase | 10→100→10 | 60s |
| **Soak Test** | Stability over time | 5 | 1 hour |
| **Smoke Test** | Quick validation | 1-2 | 30s |

---

## Repository Structure

```
Kaio-QA-portfolio-performance-test-jmeter/
├── tests/
│   ├── Kaio QA - Performance Test.jmx      # Main JMeter test plan
│   ├── jsonplaceholder-load-test.jmx       # JSONPlaceholder load test
│   ├── api-smoke-test.jmx                  # Quick smoke test
│   └── api-stress-test.jmx                 # Stress test (higher load)
├── reports/
│   ├── html-dashboard/                     # JMeter HTML Dashboard
│   ├── csv-results/                        # Raw CSV results
│   └── jtl-results/                        # JTL binary results
├── data/
│   └── test-users.csv                      # Test data for parameterization
├── .github/workflows/
│   └── jmeter.yml                          # CI/CD workflow (with Allure)
├── scripts/
│   ├── run-jmeter.sh                       # Local execution script
│   └── generate-report.sh                  # Report generation
├── jmeter.properties                        # Allure exporter config
├── package.json (for report generation)
└── README.md
```

---

## Allure Report

**Live Allure Report**: [https://qakaio.github.io/Kaio-QA-portfolio-performance-test-jmeter/allure-report/](https://qakaio.github.io/Kaio-QA-portfolio-performance-test-jmeter/allure-report/)

### Allure Features for JMeter
- **Test Trends** — Pass/fail history over time (per scenario)
- **Categories** — Tests grouped by severity, type, test plan
- **Retries** — Full retry history with timeline
- **Duration Analysis** — Slowest samplers identification
- **Charts & Metrics** — Response times, throughput, errors over time
- **Environment Info** — JMeter version, Java, test plan details

---

## How to Run

### Prerequisites
- Java 11+ (JMeter requirement)
- Apache JMeter 5.6+ installed
- `jmeter` command in PATH

### Local Execution
```bash
# 1. Clone repository
git clone https://github.com/qakaio/Kaio-QA-portfolio-performance-test-jmeter.git
cd Kaio-QA-portfolio-performance-test-jmeter

# 2. Run via command line (headless)
jmeter -n -t "tests/Kaio QA - Performance Test.jmx" -l reports/results.jtl -e -o reports/html-dashboard

# 3. Or use helper script
chmod +x scripts/run-jmeter.sh
./scripts/run-jmeter.sh "tests/Kaio QA - Performance Test.jmx"
```

### Generate HTML Dashboard
```bash
# From existing .jtl results
jmeter -g reports/results.jtl -o reports/html-dashboard

# Or use helper
./scripts/generate-report.sh reports/results.jtl
```

### Run Specific Test Plan
```bash
# Load test
jmeter -n -t tests/jsonplaceholder-load-test.jmx -l reports/load-test.jtl -e -o reports/load-test-html

# Stress test
jmeter -n -t tests/api-stress-test.jmx -l reports/stress-test.jtl -e -o reports/stress-test-html
```

---

## Allure Integration

### Configuration (`jmeter.properties`)
```properties
# Allure Report Configuration for JMeter
jmeter.reportgenerator.overall_granularity=60000
jmeter.reportgenerator.exporter.allure.classname=io.qameta.allure.jmeter.AllureExporter
jmeter.reportgenerator.outputdir=allure-results
```

### CI/CD Integration (`.github/workflows/jmeter.yml`)
```yaml
name: JMeter Performance Tests

on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM UTC
  workflow_dispatch:
    inputs:
      test_type:
        description: 'Test type to run'
        required: true
        type: choice
        options:
          - load
          - stress
          - smoke
          - all
        default: 'all'

jobs:
  test:
    name: JMeter Performance Tests
    runs-on: ubuntu-latest
    timeout-minutes: 60
    strategy:
      matrix:
        test_type: ['load', 'stress', 'smoke']
    steps:
      - uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Install JMeter
        run: |
          wget -q https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.tgz
          tar -xzf apache-jmeter-5.6.3.tgz
          echo "$PWD/apache-jmeter-5.6.3/bin" >> $GITHUB_PATH

      - name: Install Allure JMeter Plugin
        run: |
          mkdir -p $PWD/apache-jmeter-5.6.3/lib/ext
          wget -q https://repo.maven.apache.org/maven2/io/qameta/allure/allure-jmeter/2.20.0/allure-jmeter-2.20.0.jar -O $PWD/apache-jmeter-5.6.3/lib/ext/allure-jmeter-2.20.0.jar

      - name: Run JMeter Test
        run: |
          jmeter -n -t tests/${{ matrix.test_type }}.jmx -l results-${{ matrix.test_type }}.jtl -Djmeter.reportgenerator.outputdir=allure-results-${{ matrix.test_type }}

      - name: Upload Allure Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results-${{ matrix.test_type }}
          path: allure-results-${{ matrix.test_type }}
          retention-days: 7

      - name: Upload JTL Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: jmeter-results-${{ matrix.test_type }}
          path: results-${{ matrix.test_type }}.jtl
          retention-days: 30

      - name: Upload HTML Dashboard
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: jmeter-html-dashboard-${{ matrix.test_type }}
          path: html-report-${{ matrix.test_type }}/
          retention-days: 30

  allure-report:
    name: Generate Allure Report
    needs: test
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Download Allure Results
        uses: actions/download-artifact@v4
        with:
          pattern: allure-results-*
          path: allure-results
          merge-multiple: true

      - name: Generate Allure Report
        if: ${{ hashFiles('allure-results/**') != '' }}
        run: |
          npx allure generate allure-results --clean -o allure-report

      - name: Upload Allure Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-report
          path: allure-report
          retention-days: 30

      - name: Deploy Allure Report to GitHub Pages
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./allure-report
          destination_dir: allure-report
```

---

## Understanding JMeter Reports

### HTML Dashboard (JMeter Native)
- **Statistics Table** — Summary per sampler
- **Charts** — Response times, throughput, errors over time
- **Percentiles** — 50th, 90th, 95th, 99th percentile response times
- **Errors** — Detailed error breakdown

### Key Metrics to Monitor

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| **Error Rate** | <1% | 1-5% | >5% |
| **Avg Response Time** | <500ms | 500ms-2s | >2s |
| **95th Percentile** | <1s | 1-3s | >3s |
| **Throughput** | Stable | Declining | Collapsing |

---

## Allure Report vs JMeter HTML Dashboard

| Feature | JMeter HTML Dashboard | Allure Report |
|---------|----------------------|---------------|
| **Trend Analysis** | ❌ | ✅ |
| **History/Retention** | ❌ | ✅ |
| **Retry Timeline** | ❌ | ✅ |
| **Categories/Severity** | ❌ | ✅ |
| **Embedded Screenshots** | ❌ | ✅ |
| **Environment Tracking** | ❌ | ✅ |
| **CI/CD Integration** | Manual | Native |
| **Cross-Test Comparison** | ❌ | ✅ |

---

## Performance Baselines & SLI/SLO

### JSONPlaceholder API Baselines

| Endpoint | SLI (50th %ile) | SLO Target | Current |
|----------|-----------------|------------|---------|
| `GET /users` | 50ms | <100ms | 53ms ✅ |
| `GET /posts` | 120ms | <200ms | 156ms ✅ |
| `GET /comments` | 80ms | <150ms | 94ms ✅ |
| `POST /posts` | 200ms | <500ms | 312ms ✅ |

### Alerting Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| **Error Rate** | >1% | >5% |
| **95th %ile Latency** | >2s | >5s |
| **Throughput Drop** | >20% | >50% |

---

## Requirements
- **Java 11+** (JMeter 5.6+ requirement)
- **Apache JMeter 5.6+** installed
- **Memory:** `-Xms2g -Xmx4g` recommended for large tests

---

## License
MIT License — Feel free to use as reference for your own performance testing portfolio.

---

## Author
**Kaio Garcia** — Senior QA Engineer  
🔗 [GitHub](https://github.com/qakaio) • [LinkedIn](https://linkedin.com/in/kaioqa) • [Portfolio](https://qakaio.github.io)

---

## Acknowledgments
- [Apache JMeter](https://jmeter.apache.org/) for the industry-standard load testing tool
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) for the public test API
- [BlazeMeter](https://www.blazemeter.com/) for JMeter cloud execution options
- [Allure Report](https://allurereport.org/) for advanced test reporting