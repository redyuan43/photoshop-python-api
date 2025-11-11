#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成器：自动从YAML动作定义生成元数据

功能：
1. 读取actions/目录下的所有YAML文件
2. 解析动作定义
3. 生成metadata.json - 供LLM理解
4. 生成openai_functions.json - 供API调用
"""

import yaml
import json
import glob
import os
from pathlib import Path


def load_actions():
    """加载所有动作定义"""
    actions = []
    action_dir = Path(__file__).parent / "actions"
    
    # 读取所有YAML文件
    yaml_files = glob.glob(str(action_dir / "*.yaml"))
    print(f"找到 {len(yaml_files)} 个YAML文件")
    
    for file in yaml_files:
        print(f"读取: {file}")
        with open(file, 'r', encoding='utf-8') as f:
            actions_in_file = yaml.safe_load(f)
            actions.extend(actions_in_file)
    
    print(f"共加载 {len(actions)} 个动作")
    return actions


def generate_metadata(actions):
    """生成 metadata.json - 供LLM理解"""
    metadata = {}
    
    for action in actions:
        name = action['name']
        metadata[name] = {
            'category': action['category'],
            'description': action['description'],
            'aliases': action.get('aliases', []),
            'params': []
        }
        
        # 提取参数信息
        for param_name, param_config in action.get('params', {}).items():
            param_info = {
                'name': param_name,
                'type': param_config.get('type', 'string'),
                'description': param_config.get('description', ''),
                'required': param_config.get('required', False),
                'default': param_config.get('default')
            }
            metadata[name]['params'].append(param_info)
    
    return metadata


def generate_openai_functions(actions):
    """生成 openai_functions.json - 供API调用"""
    functions = []
    
    for action in actions:
        name = action['name']
        description = action['description']
        
        # 构建参数定义
        properties = {}
        required = []
        
        for param_name, param_config in action.get('params', {}).items():
            # 根据类型映射到JSON Schema
            type_mapping = {
                'float': 'number',
                'int': 'integer',
                'string': 'string',
                'bool': 'boolean',
                'object': 'object'
            }
            
            param_type = type_mapping.get(param_config.get('type', 'string'), 'string')
            
            param_info = {
                'type': param_type,
                'description': param_config.get('description', '')
            }
            
            # 如果有默认值，不设置为required
            if not param_config.get('required') and 'default' in param_config:
                pass  # 不添加到required列表
            else:
                required.append(param_name)
            
            # 如果是对象类型，需要特殊处理
            if param_type == 'object':
                param_info['properties'] = {}
                for prop_name, prop_config in param_config.get('properties', {}).items():
                    prop_type = type_mapping.get(prop_config.get('type', 'string'), 'string')
                    param_info['properties'][prop_name] = {
                        'type': prop_type,
                        'description': prop_config.get('description', '')
                    }
            
            properties[param_name] = param_info
        
        # 如果没有required参数，设置空列表
        if not required:
            required = []
        
        function = {
            'name': name,
            'description': description,
            'parameters': {
                'type': 'object',
                'properties': properties,
                'required': required
            }
        }
        
        functions.append(function)
    
    return functions


def main():
    """主函数"""
    print("=" * 60)
    print("生成器：自动生成元数据")
    print("=" * 60)
    
    # 创建artifacts目录
    artifacts_dir = Path(__file__).parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    
    # 加载动作
    actions = load_actions()
    
    # 生成metadata.json
    print("\n[1] 生成 metadata.json...")
    metadata = generate_metadata(actions)
    metadata_file = artifacts_dir / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"  [OK] 保存到: {metadata_file}")
    
    # 生成openai_functions.json
    print("\n[2] 生成 openai_functions.json...")
    functions = generate_openai_functions(actions)
    functions_file = artifacts_dir / "openai_functions.json"
    with open(functions_file, 'w', encoding='utf-8') as f:
        json.dump(functions, f, ensure_ascii=False, indent=2)
    print(f"  [OK] 保存到: {functions_file}")
    
    # 统计信息
    print("\n" + "=" * 60)
    print(f"生成完成！")
    print(f"  动作总数: {len(actions)}")
    print(f"  metadata.json: {len(metadata)} 个动作")
    print(f"  openai_functions.json: {len(functions)} 个函数")
    print("=" * 60)
    
    # 显示所有动作
    print("\n动作列表:")
    categories = {}
    for action in actions:
        cat = action['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(action['name'])
    
    for cat, names in sorted(categories.items()):
        print(f"\n  [{cat}] ({len(names)}个)")
        for name in sorted(names):
            print(f"    - {name}")


if __name__ == "__main__":
    main()
