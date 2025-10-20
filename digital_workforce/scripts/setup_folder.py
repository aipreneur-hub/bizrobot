import os

# ----------------------------------------------------------------------
# Utility to create the Digital Workforce Framework folder structure
# ----------------------------------------------------------------------

PROJECT_STRUCTURE = {
    "digital_workforce": {
        "README.md": "",
        "pyproject.toml": "",
        "requirements.txt": "",
        ".env": "",
        ".gitignore": "",
        "src": {
            "digital_workforce": {
                "__init__.py": "",
                "main.py": "# Entry point for cognitive worker runtime\n",
                "config.py": "# Global configuration and settings\n",

                "core": {
                    "__init__.py": "",
                    "cognitive_graph.py": "# LangGraph cognitive loop\n",
                    "node_types": {
                        "__init__.py": "",
                        "perceive_node.py": "",
                        "plan_node.py": "",
                        "decision_node.py": "",
                        "action_node.py": "",
                        "reflect_node.py": ""
                    },
                    "guards": {
                        "__init__.py": "",
                        "policy_guard.py": "",
                        "bias_guard.py": "",
                        "confidence_guard.py": ""
                    },
                    "runtime": {
                        "__init__.py": "",
                        "checkpoint.py": "",
                        "executor.py": "",
                        "contracts.py": ""
                    },
                },

                "decision_engine": {
                    "__init__.py": "",
                    "api.py": "",
                    "registry.py": "",
                    "evaluator.py": "",
                    "filters_engine.py": "",
                    "roi_evaluator.py": "",
                    "feedback_manager.py": "",
                    "decision_projects": {
                        "__init__.py": "",
                        "approve_invoice.yaml": """project_id: approve_invoice
description: Auto-approve vendor invoices < ₺5,000 if trusted vendor and compliant.
inputs: [vendor, amount, vat]
filters: [policy_filter, bias_filter, risk_filter]
decision_logic:
  - if: amount < 5000 and vendor.trust_score > 0.8
    then: approve
  - else: hold
roi_metrics:
  cost_saved_per_auto_approval: 2.5
  accuracy_weight: 0.9
feedback_rules:
  update_threshold_if_hitl_overrides: 3
""",
                        "match_bank_txn.yaml": "",
                        "submit_vat.yaml": ""
                    }
                },

                "mcp": {
                    "__init__.py": "",
                    "registry.py": "",
                    "tool_executor.py": "",
                    "connectors": {
                        "__init__.py": "",
                        "erp_connector.py": "",
                        "bank_connector.py": "",
                        "tax_connector.py": "",
                        "file_connector.py": ""
                    }
                },

                "memory": {
                    "__init__.py": "",
                    "episodic_store.py": "",
                    "semantic_store.py": "",
                    "policy_store.py": ""
                },

                "audit": {
                    "__init__.py": "",
                    "audit_log.py": "",
                    "roi_tracker.py": "",
                    "feedback_processor.py": ""
                },

                "interfaces": {
                    "__init__.py": "",
                    "perception_interface.py": "",
                    "decision_interface.py": "",
                    "tool_interface.py": ""
                },

                "models": {
                    "__init__.py": "",
                    "decision_model.py": "",
                    "cognitive_state.py": "",
                    "action_model.py": "",
                    "reflection_model.py": ""
                },

                "utils": {
                    "__init__.py": "",
                    "logger.py": "",
                    "tracing.py": "",
                    "yaml_loader.py": "",
                    "expression_parser.py": ""
                },

                "tests": {
                    "__init__.py": "",
                    "test_decision_engine.py": "",
                    "test_cognitive_graph.py": "",
                    "test_mcp_registry.py": "",
                    "test_feedback_learning.py": ""
                },

                "examples": {
                    "__init__.py": "",
                    "digital_accountant.py": "",
                    "goal_invoice_processing.yaml": ""
                },
            },
        },
        "scripts": {
            "create_structure.py": "# Bootstrap utility\n",
            "seed_decision_projects.py": "",
            "run_dev.sh": "#!/bin/bash\n# Launch local dev environment\n"
        }
    }
}


def create_items(base_path, structure):
    """Recursively create directories and files"""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_items(path, content)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content or "")


def main():
    base_dir = os.getcwd()
    create_items(base_dir, PROJECT_STRUCTURE)
    print(f"✅ Digital Workforce Framework created at: {base_dir}/digital_workforce")


if __name__ == "__main__":
    main()
