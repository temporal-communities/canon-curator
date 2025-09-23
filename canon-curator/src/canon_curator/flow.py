from prefect import flow, task


@task
def extract():
    pass


@task()
def enrich():
    pass


@task
def merge():
    pass


@task
def validate():
    pass


@task
def load():
    pass


@flow(name="enrichment-pipeline")
def enrichment_pipeline():
    pass


if __name__ == "__main__":
    enrichment_pipeline()
