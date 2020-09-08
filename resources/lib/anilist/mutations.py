# -*- coding: utf-8 -*-

# Publish a new text activity
# variables: $text: String
# example: { 'text': "Hello, world!" }
mutationForSaveTextActivity = '''
    mutation ($text: String) {
        SaveTextActivity(text: $text) {
            id
            text
            isLocked
        }
    }
'''

mutationForUpdatingAnime = '''
    mutation ($id: Int, $newProgress: Int) {
        SaveMediaListEntry(id: $id, progress: $newProgress){
            id
            mediaId
            progress
            notes
        }
    }
'''
