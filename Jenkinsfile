node ('docker') {
    try {
        env.TAG = "$BUILD_TIMESTAMP-$BUILD_ID"
        env.BASE_X86 = "jfloff/alpine-python"
        env.BASE_ARM = "resin/raspberry-pi-alpine-python"
        env.IMAGE_X86 = "sdelrio/claymore-exporter"
        env.IMAGE_ARM = "sdelrio/claymore-exporter-arm"

        stage("Checkout") {
            currentBuild.displayName = "$TAG"
            // currentBuild.description = "Description $BUILD_ID"
            notifyBuild('STARTED')
            sh 'echo Current Build: $BUILD_TIMESTAMP-$BUILD_ID'
            checkout scm
        }

        stage("Build") {
            parallel b_intel: {
                sh "echo X86=${BASE_X86}"
                sh 'docker version'
                sh "docker build --build-arg BASE_IMAGE=${BASE_X86} -t ${IMAGE_X86}:${TAG} ."
                sh "docker run --rm --entrypoint uname ${IMAGE_X86}:${TAG} -m"
            },
            b_arm: {
                sh "echo ARM=${BASE_ARM}"
                sh 'docker version'
                sh "docker build --build-arg BASE_IMAGE=${BASE_ARM} -t ${IMAGE_ARM}:${TAG} ."
                sh "docker run --rm --entrypoint uname ${IMAGE_ARM}:${TAG} -m"
            }
        }

        stage("Unit Test") {
            parallel u_intel: {
                sh "docker run --name claymore_intel_${TAG} --entrypoint pytest ${IMAGE_X86}:${TAG} --junitxml TEST-unit-intel.xml"
                sh "docker cp claymore_intel_${TAG}:/usr/local/bin/TEST-unit-intel.xml ."
                sh "docker rm claymore_intel_${TAG}"
            },
            u_arm: {
                sh "docker run --name claymore_arm_${TAG} --entrypoint pytest ${IMAGE_ARM}:${TAG} --junitxml TEST-unit-arm.xml"
                sh "docker cp claymore_arm_${TAG}:/usr/local/bin/TEST-unit-arm.xml ."
                sh "docker rm claymore_arm_${TAG}"
            }
            junit 'TEST-*.xml'
        }

        stage("Push") {
            withCredentials([usernamePassword(
            credentialsId: 'docker-hub', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER'
            )]) {
                sh "docker login --username $DOCKER_USER --password $DOCKER_PASS"
                parallel p_intel: {
                    sh "echo docker push ${IMAGE_X86}:${TAG}"
                },
                p_arm: {
                    sh "echo docker push ${IMAGE_ARM}:${TAG}"
                }
            }
        }

    } catch (e) {
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        throw e
    } finally  {
        // Success or failure, always send notifications
        notifyBuild(currentBuild.result)
        stage("Cleanup") {
            sh 'docker rmi ${IMG_X86}:${TAG}'
            sh 'docker rmi ${IMG_ARM}:${TAG}'
        }
    }
}

def notifyBuild(String buildStatus = 'STARTED') {
    // build status of null means successful
    buildStatus =  buildStatus ?: 'SUCCESSFUL'

    // Default values
    def colorName = 'RED'
    def colorCode = '#FF0000'
    def subject = "${buildStatus}: Job '${env.JOB_NAME} [${env.TAG}]'"
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
    slackSend (color: colorCode, message: subject)

}
