# Schreiben der Fritzbox Anruferliste in eine CSV Datei

## AVM

## Requirements:

This plugin has no requirements or dependencies. It is completely based on the TR-064 interface from AVM (http://avm.de/service/schnittstellen/)

I have tested it with a FritzBox 7490 (FRITZ!OS 06.51), a FRITZ! WLAN Repeater 1750E (FRITZ!OS 06.32) and a WLAN Repeater 300E (FRITZ!OS 06.30).

**README.md:** https://github.com/smarthomeNG/plugins/tree/develop/avm

**Thread to the plugin:** https://knx-user-forum.de/forum/supportforen/smarthome-py/934835-avm-plugin

## Access to Fritzbox CallMonitor:

The CallMonitor of the FRITZ!Box is a service running on port 1012 and provides information on incoming, outgoing, and active calls. It can be viewed by doing a `telnet fritz.box 1012`. The CallMonitor needs to be activated by calling `#96*5*` on a phone, which is directly connected to the FritzDevice. The CallMonitor can be again deactivated by calling `#96*4*`.  
The MonitoringService (a dedicated thread of this plugin, which listens to the CallMonitor) currently is able to detect the last incoming and the last outgoing call. It is not 100% possible to detect the last missed call, so this feature is not available. 

## Further possibilities: Integration of calllist into SmartVISU:

Logik (fritzbox_7490 ist der Name der Plugin-Instanz):

../etc/logics.yaml:

```yaml
CallListCSVLogic:
    filename: calllist_csv_logic.py
    watch_item: avm.monitor.newest.event # am Beispiel des neusten Events im Callmonitor (incoming oder outgoing)
```

../logics/calllist_csv_logic.py:

```python
#!/usr/bin/env python3
# calllist_csv_logic.py

 import csv 
 if sh.avm.monitor.newest.event() == 'disconnect':
     with open('/var/www/smartvisu/temp/calllist.csv', 'w') as csvfile:
         fieldnames = ['Device', 'Duration', 'Port', 'CalledNumber', 'Name', 'Date', 'Numbertype', 'Caller', 'Type', 'Id', 'Called']
         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
         writer.writeheader()
         calllist = sh.fritzbox_7490.get_calllist()
         if not calllist is None:
             if len(calllist) > 0:
                 if not calllist[0] is None:
                     for element in calllist:
                         writer.writerow(element)
```

PHP Code (lib/phone/service/avm_sv.php) -> muss via Konfig dann ausgewählt werden!

```php
 <?php
 require_once '../../../lib/includes.php';
 require_once const_path_system.'phone/phone.php';
 
 
 /**
  * This class reads the phonelist of a fritzbox (tested with 7490)
  */
 class phone_avm extends phone
 {
 	private $csv;
 
 	/**
 	 *
 	 */
 	private function my_str_getcsv($input, $delimiter = ',', $enclosure = '"', $escape = null, $eol = null)
 	{
 		$temp = fopen("php://memory", "rw");
 		fwrite($temp, $input);
 		fseek($temp, 0);
 		$r = array();
 		while (($data = fgetcsv($temp, 4096, $delimiter, $enclosure)) !== false)
 		{
 			$r[] = $data;
 		}
 
 		fclose($temp);
 
 		return $r;
 	}
 
 	/**
 	 *
 	 */
 	private function handlecsv()
 	{
 		// cut off the first header line
 		$this->csv = preg_replace("/^(.*\n){1}/", "", $this->csv);
 
 		// convert into array
 		$this->csv = $this->my_str_getcsv($this->csv);   
 		$this->debug($this->csv, "csv");
 
 		$i = 1;
 		foreach ($this->csv as $parts)
 		{
                         
                        $date = trim($parts[5]);
 			$date = substr($date, 0, 16);                        
                    
 			$this->data[] = array(
 				'pos' => $i++,
 				'dir' => (trim($parts[8]) == 1 ? 1 : (trim($parts[8]) == 2 ? 0 : -1)),
 				'date' => $date,
 				'number' => (trim($parts[8]) == 1 ? $parts[7] : (trim($parts[8]) == 2 ? $parts[7] : $parts[10])),
 				'name' => $parts[4],
 				'called' => $parts[10],
 				'duration' => $parts[1]
 			);
                         
 		}
                 
 	}
 
 	/**
 	 *
 	 */
 	public function run()
 	{		
 		// get csv
 		$this->csv = file_get_contents('/var/www/smartvisu/temp/calllist.csv');
 
 		// handle csv
 		if (strlen($this->csv) > 10)
 			$this->handlecsv();
 
 		// free vals	
 		$this->csv = '';
 	}
 
 	} // class end
 
 
 	// -----------------------------------------------------------------------------
 	// call the service
 	// -----------------------------------------------------------------------------
 
 	$service = new phone_avm(array_merge($_GET, $_POST));
 	echo $service->json();
 
 	?>

```
 