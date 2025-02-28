FROM public.ecr.aws/lambda/python:3.13

# Install Python dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY lambdas/db_manager/db_manager.py \
  ${LAMBDA_TASK_ROOT}/

# Copy migrations
COPY alembic.ini ${LAMBDA_TASK_ROOT}/
COPY migrations ${LAMBDA_TASK_ROOT}/migrations

# Copy database code
COPY database ${LAMBDA_TASK_ROOT}/database

CMD [ "db_manager.handler" ]
