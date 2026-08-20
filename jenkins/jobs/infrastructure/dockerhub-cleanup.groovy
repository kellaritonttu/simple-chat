@Library('shared') _

pipeline {
    agent any

    parameters {
        string(name: 'REPO',      defaultValue: 'simple-chat-backend', description: 'Docker Hub repo name')
        string(name: 'USERNAME',  defaultValue: 'harhatilatonttu',     description: 'Docker Hub username')
        string(name: 'KEEP_LAST', defaultValue: '3',                   description: 'Number of tags to keep')
    }

    stages {
        stage('Prune tags') {
            steps {
                pruneDockerTags(
                    username: params.USERNAME,
                    repo:     params.REPO,
                    keepLast:  params.KEEP_LAST.toInteger()
                )
            }
        }
    }
}