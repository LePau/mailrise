build:
	docker build -t lepau/mailrise:1.4.0j -f Dockerfile .

deploy: build
	# docker login ghcr.io -u LePau # GITHUB_IMAGE_REGISTRY_PASSWORD
	docker tag lepau/mailrise:1.4.0j ghcr.io/lepau/mailrise:1.4.0j
	docker push ghcr.io/lepau/mailrise:1.4.0j
