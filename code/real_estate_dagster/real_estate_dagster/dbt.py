from dagster import job, op, OpExecutionContext, Field, String

from dagster_dbt import dbt_cli_resource


def _dbt_run(context: OpExecutionContext, project_dir: String):
    context.log.info(f"elt: executing dbt run with project_dir: '{project_dir}'")
    context.resources.dbt.cli("run", project_dir=project_dir)

def _dbt_test(context: OpExecutionContext, project_dir: String):
    context.log.info(f"elt: executing dbt test with project_dir: '{project_dir}'")
    context.resources.dbt.cli("test", project_dir=project_dir)

def _dbt_generate_docs(context: OpExecutionContext, project_dir: String):
    context.log.info(f"elt: executing dbt docs generate with project_dir: '{project_dir}'")
    context.resources.dbt.cli("docs generate", project_dir=project_dir)

def _dbt_source_freshness(context: OpExecutionContext, project_dir: String):
    context.log.info(f"elt: executing dbt source freshness with project_dir: '{project_dir}'")
    context.resources.dbt.cli("source freshness", project_dir=project_dir)


@op(required_resource_keys={'dbt'}, config_schema={'project_dir': Field(String)})
def dbt_bronze_run_op(context: OpExecutionContext, dependent_job=None):
    project_dir = context.op_config.get('project_dir')
    _dbt_run(context, project_dir)
    
@op(required_resource_keys={'dbt'}, config_schema={'project_dir': Field(String)})
def dbt_bronze_test_doc_sources_op(context: OpExecutionContext, dependent_job=None):
    project_dir = context.op_config.get('project_dir')
    _dbt_test(context, project_dir)
    _dbt_generate_docs(context, project_dir)
    _dbt_source_freshness(context, project_dir)


@op(required_resource_keys={'dbt'}, config_schema={'project_dir': Field(String)})
def dbt_silver_run_op(context: OpExecutionContext, dependent_job=None):
    project_dir = context.op_config.get('project_dir')
    _dbt_run(context, project_dir)

@op(required_resource_keys={'dbt'}, config_schema={'project_dir': Field(String)})
def dbt_silver_test_doc_sources_op(context: OpExecutionContext, dependent_job=None):
    project_dir = context.op_config.get('project_dir')
    _dbt_test(context, project_dir)
    _dbt_generate_docs(context, project_dir)
    _dbt_source_freshness(context, project_dir)


@op(required_resource_keys={'dbt'}, config_schema={'project_dir': Field(String)})
def dbt_gold_run_op(context: OpExecutionContext, dependent_job=None):
    project_dir = context.op_config.get('project_dir')
    _dbt_run(context, project_dir)

@op(required_resource_keys={'dbt'}, config_schema={'project_dir': Field(String)})
def dbt_gold_test_doc_sources_op(context: OpExecutionContext, dependent_job=None):
    project_dir = context.op_config.get('project_dir')
    _dbt_test(context, project_dir)
    _dbt_generate_docs(context, project_dir)
    _dbt_source_freshness(context, project_dir)


@job(resource_defs={'dbt': dbt_cli_resource})
def dbt_bronze():
    dbt_bronze_test_doc_sources_op(dbt_bronze_run_op())


@job(resource_defs={'dbt': dbt_cli_resource})
def dbt_silver():    
    dbt_silver_test_doc_sources_op(dbt_silver_run_op())

@job(resource_defs={'dbt': dbt_cli_resource})
def dbt_gold():    
    dbt_gold_test_doc_sources_op(dbt_gold_run_op())

@job(resource_defs={'dbt': dbt_cli_resource})
def dbt_all():    
    dbt_gold_test_doc_sources_op(
        dbt_gold_run_op(
            dbt_silver_test_doc_sources_op(
                dbt_silver_run_op(
                    dbt_bronze_test_doc_sources_op(
                        dbt_bronze_run_op()
                    )
                )
            )
        )
    )