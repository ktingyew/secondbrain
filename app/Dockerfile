FROM public.ecr.aws/lambda/python:3.10

COPY index-storage /index-storage

COPY requirements.txt ./

RUN python3.10 -m pip install -r requirements.txt -t .

RUN python3.10 -c "import nltk; nltk.download('stopwords', download_dir='/nltk_data')"

ENV NLTK_DATA=/nltk_data

COPY app.py query.py ./

CMD ["app.lambda_handler"]
