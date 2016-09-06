item = None
value = None


#?#trigger_id:cycle = 60
"""
Kommentar
"""
if logic.name == 'blockly_runner_trigger_id' and true:
  logger.info('CYCLE TRIGGER by: {}, value: {}'.format(logic.name, trigger['value'] ))
  logger.debug('BLOCKLY RUNNER TRIGGER')


#?#trigger_id2:cycle = 60
"""
Kommentar
"""
if logic.name == 'blockly_runner_trigger_id2' and true:
  logger.info('CYCLE TRIGGER by: {}, value: {}'.format(logic.name, trigger['value'] ))
  logger.debug('BLOCKLY RUNNER TRIGGER')


#?#trigger_id3:watchitem = telefon.list
if logic.name == 'blockly_runner_trigger_id3' :
  logger.info('ITEM TRIGGER id: {}, value: {}'.format(logic.name, trigger['value'] ))
  item = sh.return_item("telefon.list")
  value = sh.return_item("telefon.list")()
  logger.debug(item())sh.return_item("env.core.garbage")(True)
  ,2.2
