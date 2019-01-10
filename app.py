#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
import json

import storyscript
from storyscript.Bundle import Bundle
from storyscript.Story import Story
from storyscript.parser import Tree


def lark_tree(tree):
    resp = {}
    for item in tree.children:
        if isinstance(item, Tree):
            resp[item.data] = lark_tree(item)
        else:
            resp["value"] = item
    return resp


class Handler:
    app = Flask(__name__)

    @app.route('/lex', methods=['POST'])
    def lex():
        files = request.json['files']
        resp = {}
        for k, v in files.items():
            result = []
            tokens = Story(v).lex()
            for n, token in enumerate(tokens):
                result.append((n, token.type, token.value))
            resp[k] = result
        return jsonify(resp)

    @app.route('/parse', methods=['POST'])
    def parse():
        files = request.json['files']
        bundle = Bundle(story_files=files)
        bundle.parse(bundle.find_stories(), ebnf=None)
        resp = {}
        for k, v in bundle.stories.items():
            resp[k] = lark_tree(v)
        return jsonify(resp)

    @app.route('/compile', methods=['POST'])
    def compile():
        files = request.json['files']
        return jsonify(storyscript.load_map(files))

    @app.route('/grammar', methods=['GET'])
    def grammar():
        return storyscript.grammar()

    @app.route('/version', methods=['GET'])
    def version():
        return storyscript.__version__


def app_error(e):
    return jsonify({"message": str(e)}), 400


if __name__ == '__main__':
    handler = Handler()
    app = handler.app
    app.register_error_handler(Exception, app_error)
    app.run(host='0.0.0.0', port=8000)
