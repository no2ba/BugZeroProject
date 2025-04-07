from utils import load_translation_table, load_testcase, generate_code_from_testcase
from executor import TestExecutor
from logger import HTMLReportGenerator
import sys

def main(test_case_path=None):
    try:
        # Load test data
        translation_table = load_translation_table()
        testcase_df = load_testcase(test_case_path)
        
        # Generate and execute test script
        executor = TestExecutor()
        script_lines = generate_code_from_testcase(testcase_df, translation_table)
        results = executor.execute_script(script_lines)
        
        # Generate report
        report_path = HTMLReportGenerator.generate_report(script_lines, results)
        print(f"Report generated at: {report_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
    finally:
        executor.close()

if __name__ == "__main__":
    main()