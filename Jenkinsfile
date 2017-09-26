node ('docker') {
    try {
        def TAG="$BUILD_TIMESTAMP-$BUILD_ID"
        stage("Checkout") {
            currentBuild.displayName = "$TAG"
            // currentBuild.description = "Description $BUILD_ID"
            notifyBuild('STARTED')
            sh 'echo Current Build: $BUILD_TIMESTAMP-$BUILD_ID'
            checkout scm
        }

        stage("Build") {
            parallel b_intel: {
                def BASE_X86="jfloff/alpine-python"
                sh "export BASE_X86=jfloff/alpine-python"
                sh "echo X86=${BASE_X86}"
                sh 'docker version'
                sh "docker build --no-cache --build-arg BASE_IMAGE=${BASE_X86} -t sdelrio/claymore-exporter:${TAG} ."
                sh "docker run --entrypoint uname sdelrio/claymore-exporter:${TAG} -m"
            },
            b_arm: {
                def BASE_ARM="resin/raspberry-pi-alpine-python"
                sh "export BASE_ARM=resin/raspberry-pi-alpine-python"
                sh "echo ARM=${BASE_ARM}"
                sh 'docker version'
                sh "docker build --no-cache --build-arg BASE_IMAGE=${BASE_ARM} -t sdelrio/claymore-exporter-arm:${TAG} ."
                sh "docker run --entrypoint uname sdelrio/claymore-exporter-arm:${TAG} -m"
            }
        }

        stage("Unit Test") {
            parallel u_intel: {
                sh "docker run --name claymore_intel_${TAG} --entrypoint pytest sdelrio/claymore-exporter:${TAG} --junitxml TEST-unit-intel.xml"
                sh "docker cp claymore_intel_${TAG}:/usr/local/bin/TEST-unit-intel.xml ."
                sh "docker rm claymore_intel_${TAG}"
                junit 'TEST-unit-intel.xml'
            },
            u_arm: {
                sh "docker run --name claymore_arm_${TAG} --entrypoint pytest sdelrio/claymore-exporter-arm:${TAG} --junitxml TEST-unit-arm.xml"
                sh "docker cp claymore_arm_${TAG}:/usr/local/bin/TEST-unit-arm.xml ."
                sh "docker rm claymore_arm_${TAG}"
                junit 'TEST-unit-arm.xml'
            }
        }

        stage("Push") {
            withCredentials([usernamePassword(
            credentialsId: 'docker-hub', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER'
            )]) {
                sh "docker login --username $DOCKER_USER --password $DOCKER_PASS"
                parallel p_intel: {
                    sh "docker push sdelrio/claymore-exporter:${TAG}"
                },
                p_arm: {
                    sh "docker push sdelrio/claymore-exporter-arm:${TAG}"
                }
            }
        }

    } finally  {
        // Success or failure, always send notifications
        notifyBuild(currentBuild.result)
        stage("Cleanup") {
            sh 'docker system prune -af'
        }
    }
}

def notifyBuild(String buildStatus = 'STARTED') {
    // build status of null means successful
    buildStatus =  buildStatus ?: 'SUCCESSFUL'

    // Default values
    def colorName = 'RED'
    def colorCode = '#FF0000'
    def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
    def summary = "${subject} (${env.BUILD_URL})"

    // Override default values based on build status
    if (buildStatus == 'STARTED') {
        color = 'yellow'
        colorcode = '#ffff00'

    } else if (buildStatus == 'SUCCESSFUL') {
        color = 'GREEN'
        colorCode = '#00FF00'

    } else {
        color = 'RED'
        colorCode = '#FF0000'

    }

    // Send notifications
    slackSend (color: colorCode, message: summary)

}
