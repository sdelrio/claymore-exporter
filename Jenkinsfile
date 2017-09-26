node ('docker') {
    try {
        stage("Checkout") {
            currentBuild.displayName = "$BUILD_TIMESTAMP-$BUILD_ID"
            // currentBuild.description = "Description $BUILD_ID"
            sh 'echo Current Build: $BUILD_TIMESTAMP-$BUILD_ID'
            checkout scm
        }
        stage("Build") {
            parallel b_intel: {
                def TAG="$BUILD_TIMESTAMP-$BUIlD_ID"
                def BASE_X86="jfloff/alpine-python"
                sh "export BASE_X86=jfloff/alpine-python"
                sh "echo X86=${BASE_X86}"
                sh 'docker version'
                sh "docker build --no-cache --build-arg BASE_IMAGE=${BASE_X86} -t sdelrio/claymore-exporter:${TAG} ."
                sh "docker run --entrypoint uname sdelrio/claymore-exporter:${TAG} -m"
            },
            b_arm: {
                def TAG="$BUILD_TIMESTAMP-$BUIlD_ID"
                def BASE_ARM="resin/raspberry-pi-alpine-python"
                sh "export BASE_ARM=resin/raspberry-pi-alpine-python"
                sh "echo ARM=${BASE_ARM}"
                sh 'docker version'
                sh "docker build --no-cache --build-arg BASE_IMAGE=${BASE_ARM} -t sdelrio/claymore-exporter-arm:${TAG} ."
                sh "docker run --entrypoint uname sdelrio/claymore-exporter-arm:${TAG} -m"
            }
        }
        stage("Push") {
            withCredentials([usernamePassword(
            credentialsId: 'docker-hub', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER'
            )]) {
                sh "docker login --username $DOCKER_USER --password $DOCKER_PASS"
                parallel p_intel: {
                    def TAG="$BUILD_TIMESTAMP-$BUIlD_ID"
                    sh "docker push sdelrio/claymore-exporter:${TAG}"
                },
                p_arm: {
                    def TAG="$BUILD_TIMESTAMP-$BUIlD_ID"
                    sh "docker push sdelrio/claymore-exporter-arm:${TAG}"
                }
            }
        }


    } finally  {
        stage("Cleanup") {
            sh 'docker system prune -af'
        }
    }
}
