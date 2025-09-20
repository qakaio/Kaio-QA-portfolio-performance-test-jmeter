# 🚀 JMeter Performance Testing

![JMeter](https://img.shields.io/badge/Tool-JMeter-red) ![Language](https://img.shields.io/badge/Language-XML-blue) ![License](https://img.shields.io/badge/License-MIT-green)

This repository contains **performance testing scripts and reports** created using **Apache JMeter**. The tests evaluate the responsiveness, stability, and scalability of APIs and web applications under different load conditions.

---

## 📊 Test Example

In a test with **10 simultaneous users** on the public API **JSONPlaceholder**:  

- **Average response time:** 375 ms  
- **Minimum response time:** 55 ms  
- **Maximum response time:** 1425 ms  
- **Error rate:** 0%  
- **Throughput:** 2.3 requests/sec  
- **Data transfer rate:** 15.44 KB/s  

✅ These results indicate that the API remained stable under the applied load, with acceptable response times for the simulated users. Despite the peak of 1425 ms, the **average response time remained consistent**, demonstrating that the API can handle multiple simultaneous requests without failures.

---

## ✨ Features

- Load testing with multiple virtual users  
- Monitoring response times, throughput, and error rates  
- Generating detailed performance reports  
- Configurable test plans for different scenarios  

---

## 🛠 How to Run the Tests

1. **Install JMeter**: [Apache JMeter](https://jmeter.apache.org/download_jmeter.cgi)  
2. **Clone this repository**:  
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```  
3. **Open the `.jmx` test plan** in JMeter  
4. **Adjust parameters** (number of users, ramp-up time, loops, etc.) as needed  
5. **Run the test** by clicking the **Start** button  
6. **Analyze the results** using listeners or export them as HTML/CSV reports  

---

## 📂 Repository Structure

```
/tests
   └── test-plan.jmx       # JMeter test plan
/reports
   └── example-report.html # Sample performance report
/README.md                 # Project documentation
```

---

## ⚡ Conclusion

This project demonstrates the ability to **evaluate and report on API performance**, helping QA engineers and developers identify bottlenecks, improve responsiveness, and ensure stability under load.
