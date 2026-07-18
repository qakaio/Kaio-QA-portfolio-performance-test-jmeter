#!/usr/bin/env python3
"""
Convert JMeter JTL results to Allure results JSON files.
Supports both CSV and XML JTL formats.
Each JMeter sampler becomes an Allure test case.

Usage:
    python scripts/jtl_to_allure.py <jtl_file> [--output-dir allure-results]
"""

import os
import sys
import json
import time
import uuid
import csv
import argparse
import xml.etree.ElementTree as ET


def parse_jtl_xml(jtl_path):
    """Parse JTL XML file and return list of test case dicts."""
    tree = ET.parse(jtl_path)
    root = tree.getroot()

    test_cases = []
    for i, sample in enumerate(root.findall(".//httpSample"), start=1):
        tc = {
            "name": sample.get("lb", f"HTTP Request {i}"),
            "status": "passed" if sample.get("s") == "true" else "failed",
            "duration_ms": int(float(sample.get("t", 0))),
            "response_code": sample.get("rc", ""),
            "response_message": sample.get("rm", ""),
            "url": sample.get("lt", ""),
            "thread_name": sample.get("tn", ""),
            "timestamp": int(float(sample.get("ts", time.time() * 1000))),
            "assertion_result": None,
        }

        assertion = sample.find(".//assertionResult")
        if assertion is not None:
            assertion_name = assertion.findtext("name", "")
            assertion_failure = assertion.findtext("failure", "false")
            assertion_error = assertion.findtext("error", "false")
            if assertion_failure == "true" or assertion_error == "true":
                tc["status"] = "failed"
                tc["assertion_result"] = {
                    "name": assertion_name,
                    "failure_message": assertion.findtext("failureMessage", ""),
                }

        test_cases.append(tc)

    return test_cases


def parse_jtl_csv(jtl_path):
    """Parse JTL CSV file and return list of test case dicts."""
    test_cases = []
    with open(jtl_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            tc = {
                "name": row.get("label", f"HTTP Request {i}"),
                "status": "passed" if row.get("success", "true") == "true" else "failed",
                "duration_ms": int(float(row.get("elapsed", 0))),
                "response_code": row.get("responseCode", ""),
                "response_message": row.get("responseMessage", ""),
                "url": row.get("URL", ""),
                "thread_name": row.get("threadName", ""),
                "timestamp": int(float(row.get("timeStamp", time.time() * 1000))),
                "assertion_result": None,
            }

            failure_msg = row.get("failureMessage", "")
            if failure_msg:
                tc["status"] = "failed"
                tc["assertion_result"] = {
                    "name": row.get("assertionName", "Assertion"),
                    "failure_message": failure_msg,
                }

            test_cases.append(tc)

    return test_cases


def parse_jtl(jtl_path):
    """Parse JTL file - auto-detect CSV vs XML format."""
    with open(jtl_path, "r") as f:
        first_char = f.read(1)
    
    if first_char == "<":
        return parse_jtl_xml(jtl_path)
    else:
        return parse_jtl_csv(jtl_path)


def create_allure_result(tc, suite_name="JMeter Performance Tests"):
    """Create an Allure result JSON object from a test case."""
    allure_result = {
        "name": tc["name"],
        "status": tc["status"],
        "stage": "finished",
        "type": "test",
        "suites": [{"name": suite_name}],
        "start": tc["timestamp"],
        "stop": tc["timestamp"] + tc["duration_ms"],
        "uuid": str(uuid.uuid4()),
        "historyId": str(uuid.uuid4()),
        "labels": [
            {"name": "suite", "value": suite_name},
            {"name": "thread", "value": tc["thread_name"]},
            {"name": "host", "value": "github-actions"},
            {"name": "framework", "value": "JMeter"},
        ],
        "steps": [
            {
                "name": f"HTTP Request: {tc['name']}",
                "status": tc["status"],
                "stage": "finished",
                "start": tc["timestamp"],
                "stop": tc["timestamp"] + tc["duration_ms"],
                "statusDetails": {
                    "message": f"Response: {tc['response_code']} {tc['response_message']}"
                },
            }
        ],
    }

    if tc["status"] == "failed" and tc.get("assertion_result"):
        allure_result["statusDetails"] = {
            "message": tc["assertion_result"]["failure_message"],
            "known": False,
            "flaky": False,
        }
    elif tc["status"] == "failed":
        allure_result["statusDetails"] = {
            "message": f"HTTP {tc['response_code']}: {tc['response_message']}",
            "known": False,
            "flaky": False,
        }

    return allure_result


def main():
    parser = argparse.ArgumentParser(description="Convert JMeter JTL to Allure results")
    parser.add_argument("jtl_file", help="Path to the JTL file")
    parser.add_argument("--output-dir", default="allure-results", help="Output directory for allure results")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    test_cases = parse_jtl(args.jtl_file)
    print(f"Parsed {len(test_cases)} test cases from {args.jtl_file}")

    suite_name = os.path.basename(args.jtl_file).replace(".jtl", "").replace("-", " ").title()

    count = 0
    for tc in test_cases:
        allure_result = create_allure_result(tc, suite_name)
        result_file = os.path.join(args.output_dir, f"{tc['status']}-{tc['name'].replace('/', '_')}-{uuid.uuid4().hex[:8]}.json")
        with open(result_file, "w") as f:
            json.dump(allure_result, f, indent=2)
        count += 1

    env_file = os.path.join(args.output_dir, "environment.properties")
    with open(env_file, "w") as f:
        f.write("framework=JMeter\n")
        f.write("language=Python (JTL converter)\n")
        f.write("project=Kaio-QA-portfolio-performance-test-jmeter\n")
        f.write("repo=https://github.com/qakaio/Kaio-QA-portfolio-performance-test-jmeter\n")
        f.write(f"suite={suite_name}\n")

    print(f"Generated {count} Allure result files in {args.output_dir}")


if __name__ == "__main__":
    main()
