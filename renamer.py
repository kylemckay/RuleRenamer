#!/usr/bin/env python3
#This is an EXAMPLE script for parsing rule descriptions in the converted XML output from Expedition and modifying the security rule name with that value.
#This script has only been tested with security rules and has not been tested or validated with any other rule type such as decryption, NAT, etc.
#Always review the summary output and the output file to validate the changes meet your expectations.

import re
import argparse
import xml.etree.ElementTree as ET

def rename_rules_from_description(palo_file_path, output_file_path):
    """
    Loads Palo Alto XML, searches for <description> containing:
      L4 RULE: SomeRule
      L5 RULE: SomeRule
      L6 RULE: SomeRule
      L7 RULE: SomeRule
    If found, rename <entry name="old"> to <entry name="SomeRule">.
    
    Prints a summary of all changes for operator validation.
    """

    # Regex to capture "L4 RULE:", "L5 RULE:", "L6 RULE:", or "L7 RULE:"
    pattern = re.compile(r'L[4-7]\s+RULE:\s*(.+)', re.IGNORECASE)

    tree = ET.parse(palo_file_path)
    root = tree.getroot()

    # Find all <entry> tags under <rules> (covers pre-rulebase, post-rulebase, all device groups, etc.)
    entry_elems = root.findall('.//rules/entry')

    # We'll store (old_name, new_name) pairs to print after
    changes_made = []

    for entry in entry_elems:
        desc_elem = entry.find('description')
        if desc_elem is None or not desc_elem.text:
            continue

        # Because descriptions can be multiline, unify them:
        desc_text = desc_elem.text.replace('\n', ' ').replace('\r', ' ')

        match = pattern.search(desc_text)
        if match:
            # The portion after "Lx RULE:"
            new_name = match.group(1).strip()
            old_name = entry.get('name')  # current <entry> name
            if old_name != new_name:      # Only rename if different
                entry.set('name', new_name)
                changes_made.append((old_name, new_name))

    # Write the updated XML
    tree.write(output_file_path, encoding='utf-8', xml_declaration=True)

    # Print a summary of changes
    if changes_made:
        print("Summary of rule renames:")
        for old_n, new_n in changes_made:
            print(f"  {old_n}  -->  {new_n}")
    else:
        print("No rules were renamed.")

def main():
    parser = argparse.ArgumentParser(
        description="Rename Palo Alto rules by matching 'L4 RULE:', 'L5 RULE:', 'L6 RULE:', or 'L7 RULE:' text in <description>, with a summary of changes."
    )
    parser.add_argument('palo_file', help="Path to the original Palo Alto XML (e.g. config.xml)")
    parser.add_argument('output_file', help="Path to the output XML file after renaming")
    args = parser.parse_args()

    rename_rules_from_description(args.palo_file, args.output_file)

    print(f"Done. Updated XML written to {args.output_file}")

if __name__ == '__main__':
    main()
