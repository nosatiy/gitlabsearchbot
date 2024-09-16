def get_projects_query(end_point):
    string = (
        '''
          query{
            projects(search: "", after:"'''
        + end_point
        + """"){
              count,
              pageInfo{
                endCursor,
                hasNextPage,
                hasPreviousPage,
                startCursor
              },
              nodes{
                fullPath,
                id,
                repository{
                  tree(recursive: true, ref: "master"){
                    blobs{
                      pageInfo{
                        hasNextPage,
                        endCursor
                      },
                      nodes{
                        path,
                        flatPath,
                        webUrl
                      }
                    }
                  }
                }
              }
            }
          }

"""
    )
    return string


def get_incomplited_project_query(project_path, end_point):
    string = (
        '''
          query{
            project(fullPath: "'''
        + project_path
        + '''")
            {
              fullPath
              repository{
                tree(recursive: true, ref: "master"){
                  blobs(after: "'''
        + end_point
        + """"){
                    nodes{
                      path
                    }
                    pageInfo{
                      hasNextPage
                      endCursor
                    }
                  }
                }
              }   
            }
          }
"""
    )
    return string


def get_project_blobs_query(project_path, blops):
    string = (
        '''
          query{  
            project(fullPath: "'''
        + project_path
        + """"){
              fullPath
              repository{
                blobs(paths: ["""
          + blops
          + """], ref: "master"){
                  nodes{
                    path,
                    rawPath,
                    rawBlob,
                  }
                }
              }
            }
          }
"""
    )
    return string
