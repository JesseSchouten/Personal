# Description
This is a quick and small tutorial followed from https://spring.io/guides/gs/accessing-data-mysql/#initial. On of the characteristics of the 
spring framework is the structure in which the data objects are placed: Controller, Service, Repository & Dao. 

## Tools used:
   * Docker
   * Java
   * Spring
   
## Steps:
See https://spring.io/guides/gs/accessing-data-mysql/#initial.

To spin up the docker container:
- Nagivate to data-mysql\complete
- docker-compose -f docker-compose.yml up
- docker exec -it container-name bash
	- Check container name using docker container ls
	
To build the project with maven:
- install maven from https://maven.apache.org/download.cgi
	- pick the Binary zip archive version.
	To get it to work, I had to add this to the PATH variable, as well as manually add the jdk to the JAVA_PATH variable.
- Navigate to data-mysql\complete
- mvn spring-boot:run




