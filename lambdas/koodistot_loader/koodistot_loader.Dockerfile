FROM public.ecr.aws/lambda/python:3.12

# Install Python dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy function code
COPY lambdas/koodistot_loader/koodistot_loader.py ${LAMBDA_TASK_ROOT}

COPY database/db_helper.py \
    database/base.py \
    database/codes.py \
    database/models.py  \
    ${LAMBDA_TASK_ROOT}/database/

CMD [ "koodistot_loader.handler" ]
