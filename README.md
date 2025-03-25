# RuleRenamer
Palo Alto NGFW XML Rule Renamer

This is an EXAMPLE script for parsing rule descriptions in the converted XML output from Expedition and modifying the security rule name with that value. The script has only been tested with security rules and has not been tested or validated with any other rule type such as decryption, NAT, etc. Always review the summary output and the output file to validate the changes meet your expectations.

Run the script as follows: <br/>
python3 renamer.py <input.xml> <output.xml>

Where <input.xml> is the Converted XML file from Expedition and <output.xml> is the desired output file name in XML format.

After completion, the script will summarize the list of changes made, for example:

Summary of rule renames: <br/>
  NGFW_ONBOX_ACL_1  -->  Inside_Outside_Rule  <br/>
  NGFW_ONBOX_ACL_2  -->  Custom-Rule1  <br/>
  NGFW_ONBOX_ACL_3  -->  L7-Policies  <br/>
  NGFW_ONBOX_ACL_4  -->  DefaultActionRule  <br/>
Done. Updated XML written to newoutput4.xml
