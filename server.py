#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gemini MCP Server with Streaming Support
Uses the new google-genai library for better stability
"""

import json
import sys
import os

from google import genai

# Initialize client with API key
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def call_gemini_streaming(prompt: str, model_name: str = "gemini-3-pro-preview") -> str:
    """Call Gemini with streaming for better stability"""
    try:
        response_stream = client.models.generate_content_stream(
            model=model_name,
            contents=prompt,
        )

        # Collect all chunks
        full_response = ""
        for chunk in response_stream:
            if chunk.text:
                full_response += chunk.text

        return full_response
    except Exception as e:
        raise e


def handle_request(request):
    method = request.get("method")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "gemini-streaming", "version": "2.0.0"},
                "capabilities": {"tools": {}}
            }
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [{
                    "name": "ask_gemini",
                    "description": "Ask Gemini 3 Pro a question (streaming mode for stability)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The question or prompt to send to Gemini"
                            },
                            "model": {
                                "type": "string",
                                "default": "gemini-3-pro-preview",
                                "description": "Gemini model to use (default: gemini-3-pro-preview)"
                            }
                        },
                        "required": ["prompt"]
                    }
                }]
            }
        }

    elif method == "tools/call":
        args = request.get("params", {}).get("arguments", {})
        prompt = args.get("prompt", "")
        model_name = args.get("model", "gemini-3-pro-preview")

        try:
            response_text = call_gemini_streaming(prompt, model_name)

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": response_text}]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": str(e)}
            }

    # Notifications (no id) - just ignore
    if req_id is None:
        return None

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    for line in sys.stdin:
        if line.strip():
            try:
                request = json.loads(line)
                response = handle_request(request)
                if response:
                    print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                pass


if __name__ == "__main__":
    main()
