# JMeter Performance Testing Portfolio

![JMeter Tests](https://github.com/qakaio/Kaio-QA-portfolio-performance-test-jmeter/actions/workflows/jmeter.yml/badge.svg)
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
| **Reporting** | HTML Dashboard, CSV, JTL |
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
│   └── jmeter.yml                          # CI/CD workflow
├── scripts/
│   ├── run-jmeter.sh                       # Local execution script
│   └── generate-report.sh                  # Report generation
├── README.md
└── package.json (for report generation)
```

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
jmeter -n -t tests/Kaio\ QA\ -\ Performance\ Test.jmx -l reports/results.jtl -e -o reports/html-dashboard

# 3. Or use helper script
chmod +x scripts/run-jmeter.sh
./scripts/run-jmeter.sh tests/Kaio\ QA\ -\ Performance\ Test.jmx
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

## Understanding JMeter Reports

### HTML Dashboard (Recommended)
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

## CI/CD Integration

### GitHub Actions (`.github/workflows/jmeter.yml`)
```yaml
name: Performance Tests
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly Sunday 2AM
  workflow_dispatch:
    inputs:
      test-plan:
        description: 'Test plan to run'
        required: true
        type: choice
        options:
          - load
          - stress
          - smoke

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: 'temurin', java-version: '17' }
      - name: Install JMeter
        run: |
          wget -q https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.tgz
          tar -xzf apache-jmeter-5.6.3.tgz
          echo "$PWD/apache-jmeter-5.6.3/bin" >> $GITHUB_PATH
      - name: Run JMeter Test
        run: |
          jmeter -n -t tests/${{ github.event.inputs.test-plan || 'jsonplaceholder-load-test' }}.jmx -l results.jtl -e -o html-report
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: jmeter-report
          path: html-report/
```

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