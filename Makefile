IMG_NAME = "asia.gcr.io/alecsharpie/waketimes"

img-build:
	docker build -t ${IMG_NAME} .

img-run:
	docker run -e PORT=8000 -p 8000:8000 ${IMG_NAME}

img-push:
docker push ${IMG_NAME}

img-deploy:
	gcloud run deploy \
		--image ${IMG_NAME} \
		--platform managed \
		--region asia-east1 \
		--alllow-unauthenticated
