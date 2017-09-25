pipeline {
    agent {
         label "docker"
    }
    stages {
            stage("Checkout") {
               steps {
                    script {
                        currentBuild.displayName = "$BUILD_TIMESTAMP-$BUILD_ID"
                        // currentBuild.description = "Description $BUILD_ID"
                    }
                    sh 'echo Current Build: $BUILD_TIMESTAMP-$BUILD_ID'
                    checkout scm
               }
            }
//          /*   stage("Docker build") { steps {
//                 sh "docker build -t leszko/calculator:${BUILD_TIMESTAMP} ."
//
//     }  }
            stage("Build") {
                steps {
                    script {
                        def TAG="$BUILD_TIMESTAMP-$BUIlD_ID"
                        def BASE_X86="jfloff/alpine-python"
                        def BASE_ARM="resin/raspberry-pi-alpine-python"
                        sh "export BASE_X86=jfloff/alpine-python"
                        sh "export BASE_ARM=resin/raspberry-pi-alpine-python"
                        sh "echo X86=${BASE_X86}"
                        sh "echo ARM=${BASE_ARM}"
                        sh 'docker version'
                        sh "echo docker build --no-cache --build-arg BASE_IMAGE=$BASE_X86 -t sdelrio/claymore-exporter:${TAG} ."
                        sh "docker build --no-cache --build-arg BASE_IMAGE=$BASE_X86 -t sdelrio/claymore-exporter:${TAG} ."
                    }
                }
            }
    }
    post {
        always {
            sh 'docker system prune -af'
        }
    }
}
