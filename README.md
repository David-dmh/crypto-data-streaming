# expert-waddle

docker instructions:
- build image:
    - command = docker build -t property-app .
- run container from built image:
    - command = docker run --name property-app -it -p 5000:5000 -v $(pwd):/app  property-app
