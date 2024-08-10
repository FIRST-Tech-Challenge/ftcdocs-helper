import json
from datetime import datetime, timezone
from os import path
from typing import Dict, Any, Set

from sphinx.application import Sphinx
from sphinx.builders.linkcheck import CheckExternalLinksBuilder, HyperlinkAvailabilityChecker, CheckResult, HyperlinkCollector
from sphinx.util import logging
from sphinx.util.console import bold, red, yellow, green

logger = logging.getLogger(__name__)

class LinkCheckerDiffBuilder(CheckExternalLinksBuilder):
    name = 'linkcheckdiff'
    
    def init(self) -> None:
        super().init()
        self.previous_errors: Set[str] = set()
        self.current_errors: Set[CheckResult] = set()

    def load_previous_errors(self) -> None:
        try:
            with open('main-output.json', 'r') as f:
                data = json.load(f)
                self.previous_errors = set(error['uri'] for error in data.get('errors', []))
        except FileNotFoundError:
            self.previous_errors = set()
        logger.info(bold(f'Loaded {len(self.previous_errors)} previous errors'))

    def process_result(self, result: CheckResult) -> None:
        if result.status in self.config.linkcheckdiff_errors:
            self.current_errors.add(result)
            status_color = green if result.status == 'working' else red if result.status == 'broken' else yellow
            logger.info(f"{status_color(f'[{result.status.upper()}]')} {result.uri}")
            if result.message:
                logger.info(f"  Message: {result.message}")
            if result.code:
                logger.info(f"  Code: {result.code}")
            logger.info(f"  Document: {result.docname}, Line: {result.lineno}")
            logger.info('')

    def write_output(self) -> None:
        new_errors = [error for error in self.current_errors if error.uri not in self.previous_errors]
        logger.info(bold(f'New errors: {len(new_errors)}'))
        
        output = {
            "version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "errors": [
                {
                    "uri": error.uri,
                    "docname": error.docname,
                    "lineno": error.lineno,
                    "status": error.status,
                    "message": error.message,
                    "code": error.code
                }
                for error in self.current_errors
            ]
        }
        
        output_file = path.join(self.outdir, 'output.json')
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(bold(f'Output written to: {output_file}'))
        
        if new_errors:
            self.app.statuscode = 1
            logger.error(bold(red('Found new errors. Build failed.')))
        else:
            logger.info(bold(green('No new errors found. Build successful.')))

    def finish(self) -> None:
        self.load_previous_errors()
        
        checker = self.create_checker()
        logger.info(bold('Running LinkCheckerDiff...'))

        for result in checker.check(self.hyperlinks):
            self.process_result(result)
        
        self.write_output()

    def create_checker(self):
        return HyperlinkAvailabilityChecker(self.env, self.config)
    
class HyperlinkCollectorDiff(HyperlinkCollector):
    builders = ('linkcheckdiff',)
    
def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_builder(LinkCheckerDiffBuilder)
    app.add_post_transform(HyperlinkCollectorDiff)

    app.add_config_value('linkcheckdiff_errors', set(['redirected', 'broken']), [set])

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }