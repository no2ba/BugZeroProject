from pathlib import Path
from datetime import 2025
import webbrowser
from config.settings import REPORTS_DIR

class HTMLReportGenerator:
    @staticmethod
    def generate_report(script_lines, results, filename=None):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = filename or f"test_report_{timestamp}.html"
        report_path = REPORTS_DIR / filename
        
        html_content = HTMLReportGenerator._build_html(script_lines, results)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        webbrowser.open(f"file://{report_path.absolute()}")
        return str(report_path)

    @staticmethod
    def _build_html(script_lines, results):
        rows = []
        for i, (line, result) in enumerate(zip(script_lines, results), 1):
            status = "PASS" if "PASS" in result else "FAIL"
            rows.append(f"""
                <tr class='{status.lower()}'>
                    <td>{i}</td>
                    <td><code>{line}</code></td>
                    <td>{result}</td>
                </tr>
            """)
            
        return f"""
        <html>
        <head>
            <title>Test Execution Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ padding: 10px; text-align: left; border: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .pass {{ background-color: #e8f5e9; }}
                .fail {{ background-color: #ffebee; }}
                code {{ background: #f5f5f5; padding: 2px 5px; }}
                .summary {{ margin: 20px 0; padding: 15px; background: #e3f2fd; }}
            </style>
        </head>
        <body>
            <h1>Test Execution Report</h1>
            <div class="summary">
                <strong>Execution Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Total Tests:</strong> {len(results)}<br>
                <strong>Passed:</strong> {sum(1 for r in results if "PASS" in r)}<br>
                <strong>Failed:</strong> {sum(1 for r in results if "FAIL" in r)}
            </div>
            <table>
                <tr><th>Step</th><th>Command</th><th>Result</th></tr>
                {''.join(rows)}
            </table>
        </body>
        </html>
        """
