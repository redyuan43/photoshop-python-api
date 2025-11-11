#!/usr/bin/env python3
"""
自动化工件generate器
根据YAML动作定义generatemetadata.json、openai_functions.json和claude_mcp.yaml
"""

import json
import yaml
import glob
from pathlib import Path
from typing import Dict, List, Any


class ArtifactGenerator:
    """自动化工件generate器"""
    
    def __init__(self, actions_dir: str = "actions", artifacts_dir: str = "artifacts"):
        self.actions_dir = Path(actions_dir)
        self.artifacts_dir = Path(artifacts_dir)
        self.artifacts_dir.mkdir(exist_ok=True)
        
        self.actions = []
        self.metadata = {}
        self.functions = []
        self.mcp_tools = []
    
    def load_actions(self):
        """load所有YAML动作文件"""
        yaml_files = list(self.actions_dir.glob("*.yaml"))
        
        for file_path in yaml_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                actions = yaml.safe_load(f)
                self.actions.extend(actions)
        
        print(f"OK load了 {len(self.actions)} 个动作定义")
    
    def generate_metadata(self):
        """generatemetadata.json"""
        self.metadata = {}
        
        for action in self.actions:
            name = action['name']
            self.metadata[name] = {
                "category": action.get('category', ''),
                "description": action.get('description', ''),
                "params": list(action.get('params', {}).keys())
            }
        
        metadata_path = self.artifacts_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        
        print(f"OK generate metadata.json: {metadata_path}")
    
    def generate_openai_functions(self):
        """generateopenai_functions.json"""
        self.functions = []
        
        for action in self.actions:
            name = action['name']
            description = action.get('description', '')
            params_schema = action.get('params', {})
            
            # 构建properties
            properties = {}
            required = []
            
            for param_name, param_config in params_schema.items():
                param_type = param_config.get('type', 'string')
                param_desc = param_config.get('description', '')
                
                # 转换类型
                if param_type == 'int':
                    type_str = 'integer'
                elif param_type == 'float':
                    type_str = 'number'
                else:
                    type_str = 'string'
                
                properties[param_name] = {
                    "type": type_str,
                    "description": param_desc
                }
                
                if param_config.get('required', False):
                    required.append(param_name)
            
            function_def = {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": properties
                }
            }
            
            if required:
                function_def['parameters']['required'] = required
            
            self.functions.append(function_def)
        
        functions_path = self.artifacts_dir / "openai_functions.json"
        with open(functions_path, 'w', encoding='utf-8') as f:
            json.dump(self.functions, f, ensure_ascii=False, indent=2)
        
        print(f"OK generate openai_functions.json: {functions_path}")
    
    def generate_mcp_config(self):
        """generateclaude_mcp.yaml"""
        self.mcp_tools = []
        
        for action in self.actions:
            name = action['name']
            description = action.get('description', '')
            params_schema = action.get('params', {})
            
            # 构建properties
            properties = {}
            required = []
            
            for param_name, param_config in params_schema.items():
                param_type = param_config.get('type', 'string')
                param_desc = param_config.get('description', '')
                
                # 转换类型
                if param_type == 'int':
                    type_str = 'integer'
                elif param_type == 'float':
                    type_str = 'number'
                else:
                    type_str = 'string'
                
                properties[param_name] = {
                    "type": type_str,
                    "description": param_desc
                }
                
                if param_config.get('required', False):
                    required.append(param_name)
            
            tool_def = {
                "name": name,
                "description": description,
                "input_schema": {
                    "type": "object",
                    "properties": properties
                }
            }
            
            if required:
                tool_def['input_schema']['required'] = required
            
            self.mcp_tools.append(tool_def)
        
        mcp_config = {
            "name": "photoshop",
            "description": "控制Photoshop功能的接口",
            "version": "1.0.0",
            "tools": self.mcp_tools
        }
        
        mcp_path = self.artifacts_dir / "claude_mcp.yaml"
        with open(mcp_path, 'w', encoding='utf-8') as f:
            yaml.dump(mcp_config, f, default_flow_style=False, allow_unicode=True)
        
        print(f"OK generate claude_mcp.yaml: {mcp_path}")
    
    def generate_all(self):
        """generateall artifacts"""
        print("\n=== startgenerate工件 ===\n")
        
        # load动作定义
        self.load_actions()
        
        # generate各类工件
        self.generate_metadata()
        self.generate_openai_functions()
        self.generate_mcp_config()
        
        print("\n=== all artifactsgeneratecompleted ===\n")
        
        # 统计信息
        print(f"totalgenerate:")
        print(f"  - {len(self.metadata)} 个动作元数据")
        print(f"  - {len(self.functions)} 个OpenAI函数")
        print(f"  - {len(self.mcp_tools)} 个MCP工具")
        print(f"\n工件location: {self.artifacts_dir}")


if __name__ == "__main__":
    generator = ArtifactGenerator()
    generator.generate_all()
