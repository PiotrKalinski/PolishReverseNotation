from datetime import datetime
import json
import time
from subprocess import Popen, PIPE

from flask import request


def calculate_expression():
    request_data = request.data
    expressions = json.loads(request_data)['expression']

    results = []
    count = 0
    for idx, single_expression in enumerate(expressions.replace("\r", "").split("\n")):
        if idx == 0:
            count = int(single_expression)
            continue
        if idx > count:
            break
        start = time.time()
        cmd = "ruby -r \"./calculator.rb\" -e \"RPNParser.parse '{0}'\"".format(single_expression)
        end = float(time.time() - start)
        p = Popen(cmd, shell=True, stdout=PIPE)
        output, errors = p.communicate()
        request_data = output.decode("utf-8").rstrip('\n')
        results.append({"expression": single_expression, "data": request_data, "time": end})

    response = json.dumps(results, indent=4)

    with open('logs/test-{0}.txt'.format(datetime.now()), 'w') as fw:
       
        fw.write(response)

    return response