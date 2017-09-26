node ('docker') {
    try {
        stage("Checkout") {
            currentBuild.displayName = "$BUILD_TIMESTAMP-$BUILD_ID"
            // currentBuild.description = "Description $BUILD_ID"
            sh 'echo Current Build: $BUILD_TIMESTAMP-$BUILD_ID'
            checkout scm
        }
        stage("Build") {
            parallel intel: {
                def TAG="$BUILD_TIMESTAMP-$BUIlD_ID"
                def BASE_X86="jfloff/alpine-python"
                sh "export BASE_X86=jfloff/alpine-python"
                sh "echo X86=${BASE_X86}"
                sh 'docker version'
                sh "docker build --no-cache --build-arg BASE_IMAGE=${BASE_X86} -t sdelrio/claymore-exporter:${TAG} ."
                sh "docker run --entrypoint uname sdelrio/claymore-exporter:${TAG} -m"
            },
            arm: {
                def TAG="$BUILD_TIMESTAMP-$BUIlD_ID"
                def BASE_ARM="resin/raspberry-pi-alpine-python"
                sh "export BASE_ARM=resin/raspberry-pi-alpine-python"
                sh "echo ARM=${BASE_ARM}"
                sh 'docker version'
                sh "docker build --no-cache --build-arg BASE_IMAGE=${BASE_ARM} -t sdelrio/rpi-claymore-exporter:${TAG} ."
                sh "docker run --entrypoint uname sdelrio/rpi-claymore-exporter:${TAG} -m"
            }
        }
        stage("Push") {
            withCredentials([usernamePassword(credentialsId: 'docker-hub', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"
                parallel intel: {

                    def TAG="$BUILD_TIMESTAMP-$BUIlD_ID"
                    sh "docker push sdelrio/claymore-exporter:${TAG}"
                },
                arm:  {
                    def TAG="$BUILD_TIMESTAMP-$BUIlD_ID"
                    sh "docker push sdelrio/rpi-claymore-exporter:${TAG}"
                }
            }
        }


    } finally  {
        stage("Cleanup") {
            sh 'docker system prune -af'
        }
    }
}
