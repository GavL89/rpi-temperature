# RaspberryPi SenseHat Docker Image

Connects to AWS IoT to send temperatures

# Building Image
docker build -t pitemp .

# Running Image 
docker run -ti --env-file iot.env --privileged=true pitemp


# Create a .env file with variables
HOSTNAME=xxxxxxx-ats.iot.ap-southeast-2.amazonaws.com  
PRIVATEKEY=MyIotThing.private.key  
CLIENTCERTIFICATES=MyIotThing.cert.pem  
CACERTIFICATE=root-CA.crt  
CLIENTID=sdk-python-xxxxxxx  
INTERVAL=300.0
