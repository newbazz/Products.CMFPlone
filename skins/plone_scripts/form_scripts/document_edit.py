## Script (Python) "document_edit"
##parameters=text_format, field_text, file='', SafetyBelt='', choice=' Change ', field_title='', field_description='', field_id=''
##title=Edit a document
REQUEST=context.REQUEST

if not field_id:
    field_id=context.getId()
    REQUEST.set('field_id', field_id)

id, text, title, description = field_id, field_text, field_title, field_description

errors=context.validate_document_edit()

if errors:
    edit_form=getattr(context, context.getTypeInfo().getActionById( 'edit'))
    return edit_form()
    
filename=getattr(file, 'filename', '')
if file and filename:
    if filename.find('\\')>-1:       
        id=filename.split('\\')[-1]
    if filename.find('/')>-1: 
        id=filename.split('/')[-1]
else: context.plone_debug('not file ')
if not context.isIDAutoGenerated(id): 
    context.REQUEST.set('id', id)

qst='portal_status_message=Document+changed.'
REQUEST.set('portal_status_message', 'Document+changed.')

if hasattr(context, 'extended_edit'):
    edit_hook=getattr(context,'extended_edit')
    response=edit_hook(redirect=0)
    if response:
        return response
#we need to do this afterwards because metadata sets the format to the context's format
#we need to change the format to the one in the form, not the current format.
if file and filename:
    file.seek(0)

context.edit( text_format
            , text
            , file=file
            , safety_belt=SafetyBelt
            )
    
if id!=context.getId():
    context.rename_object(redirect=0, id=id)

target_action = context.getTypeInfo().getActionById( 'view' )
context.REQUEST.RESPONSE.redirect( '%s/%s?%s' % ( context.absolute_url()
                                                , target_action
                                                , qst
                                                ) )



