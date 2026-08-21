// __ folders ___________________________________________________________________
folder('infrastructure') {
    description('Infrastructure jobs')
}

folder('simple-chat') {
    description('simple-chat jobs')
}

// __ infrastructure jobs _______________________________________________________

pipelineJob('infrastructure/dockerhub-cleanup') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/kellaritonttu/jenkins-setup.git')
                    }
                    branch('main')
                }
            }
            scriptPath('jobs/infrastructure/dockerhub-cleanup.groovy')
            lightweight(false)
        }
    }
}

pipelineJob('simple-chat/backend-testing') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/kellaritonttu/simple-chat.git')
                    }
                    branch('refs/tags/v0.2.0')
                }
            }
            scriptPath('backend/Jenkinsfile.test')
            lightweight(false)
        }
    }
}

pipelineJob('simple-chat/PushRelease') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/kellaritonttu/simple-chat.git')
                    }
                    branch('refs/tags/v0.2.0')
                }
            }
            scriptPath('Jenkinsfile.pushRelease')
            lightweight(false)
        }
    }
}

pipelineJob('simple-chat/Deploy') {
    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/kellaritonttu/simple-chat.git')
                    }
                    branch('refs/tags/v0.2.0')
                }
            }
            scriptPath('Jenkinsfile.deploy')
            lightweight(false)
        }
    }
}

// Add pipelineJob definitions below:

//     pipelineJob('folder/job-name') {
//       definition {
//         cpsScm {
//           scm {
//             git {
//               remote {
//                 url('https://github.com/username/repo.git')
//               }
//               branch('branch')
//             }
//           }
//           scriptPath('path/to/Jenkinsfile')
//           lightweight(false)
//         }
//       }
//     }