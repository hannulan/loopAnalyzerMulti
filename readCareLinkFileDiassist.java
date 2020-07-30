# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 09:43:24 2020

@author: hannu
"""

# Java code from Diassist project
    private void readCarelinkFile(File file) {
        String userName = "no name";
        BufferedReader br;
        String line;
        boolean indexFound = false;
        boolean isEnglish = true;
        csvKeys = csvKeysEnglish; 
        
        /* Maps from columns in CSV to indices in the csvKeys list */
        int csvColToKey[] = new int[100];
        for (int i = 0; i < csvColToKey.length; i++)
            csvColToKey[i] = -1;

        ByteArrayOutputStream cmdByteArray[] = new ByteArrayOutputStream[csvKeys.length];
        PrintStream cmdPS[] = new PrintStream[csvKeys.length];

        for (int i = 0; i < csvKeys.length; i++) {
            cmdByteArray[i] = new ByteArrayOutputStream();
            cmdPS[i] = new PrintStream(cmdByteArray[i]);
            if (csvKeyIsString[i])
                cmdPS[i].print(csvKeys[i][1] + " = {");
            else
                cmdPS[i].print(csvKeys[i][1] + " = [");
        }

        try {
        	int row = 0; 
        	boolean readName = false; 
            br = new BufferedReader(new FileReader(file));
            // Read the first line and see if , or ; is the seperator:
            // Determine language in file by separator: , = english, ; = swedish
            line = br.readLine();
            if (line != null & row == 0) {
            	String[] itemsSemiColon = line.split("[;]"); // Swedish style
            	String[] itemsComma = line.split("[,]");     // English style
            	System.out.println("Lenght SemiColon: " + itemsSemiColon.length);
            	System.out.println("Lenght Comma: " + itemsComma.length);
            	
            	if (itemsSemiColon.length > itemsComma.length) {
            		isEnglish = false; // ie isSwedish
            		System.out.println("Is swedish");
                    csvKeys = csvKeysEnglish; 
            	}
            	else {
            		isEnglish = true;
            		System.out.println("Is english");
                    csvKeys = csvKeysEnglish; 
            	}
            } // End check of language
            
            while ((line = br.readLine()) != null) {
            	row = row +1;
            	//System.out.println("Row: " + row);
            	String[] items;
            	if (isEnglish) {
            		// Test fix strange things in csv file: 
            		line = line.replaceAll(", ",  "_");
            		line = line.replaceAll(",",  ", ");
            		items = line.split("[,]");
            	} else { // is Swedish
            		line = line.replaceAll(";",  "; ");
            		items = line.split("[;]");
            	}
            	
                
                if (items.length < 1)
                    continue;
                if (row == 1 & items.length > 1) {
                	readName = false; 
                	System.out.println("items length, row 1: " + items.length);
                	String userName1new = items[1].replace('"', ' ');
                	String userName0new = items[0].replace('"', ' ');
                	userName = userName0new + " " + userName1new; 
                	eval("userName = \"" + userName + "\";");
                }
                if (items[0].equalsIgnoreCase("Name")) {
                	System.out.println("Name found");
                    userName = items[1];
                    if(userName.substring(0,1).equals("\"")) eval("userName = " + userName + ";"); // If username is quoted with "
                    else eval("userName = \"" + userName + "\";");
                    readName = true; 
                }
//                else if (items[0].equalsIgnoreCase("Last name"))  {
//                    readName = true; 
//                }
                else if (items[0].equalsIgnoreCase("Index")) {
                    System.out.println("Index found");
                	indexFound = true;
                    /* Find all mapping from csvColumn to keys */
                    findColumnKeys: for (int i = 0; i < items.length; i++) {
                        String item = items[i];
                        if (item.subSequence(0, 1).equals("\"")) {
                            item = item.substring(1, item.length() - 1);
                        }
                        for (int j = 0; j < csvKeys.length; j++) {
                            if (item.equalsIgnoreCase(csvKeys[j][0])) {
                                csvColToKey[i] = j;
                                continue findColumnKeys;
                            }
                        }
                    }
                    continue;
                } else if (indexFound) {	
                    for (int i = 0; i < items.length; i++) {
                        if (csvColToKey[i] != -1) {
                            int key = csvColToKey[i];
                            if (key == csvKey_Date) {
                                items[i] = items[i].replace('/', '-');
                                //if (isEnglish)
                                	items[i] = items[i].substring(1, 11); // To remove a first empty character.
                                	//} 
                            } else if (key == csvKey_Time && !items[1].equals("")) {
                                items[i] = items[i].substring(1, 6);
                            }
                            if (items[i].equals(" ")) {
                                if (csvKeyIsString[key]) {
                                    cmdPS[key].print("\"\",");
                                } else {
                                    cmdPS[key].print("0.0,");
                                }
                            } else {
                                if (csvKeyIsString[key]) {
                                    cmdPS[key].print("\"" + items[i] + "\",");
                                } else {
                                    cmdPS[key].print(items[i].replace(",", ".") + ",");
                                }

                            }

                        }
                    }
                }
            }
            for (int i = 0; i < csvKeys.length; i++) {
                if (csvKeyIsString[i])
                    cmdPS[i].print("};");
                else
                    cmdPS[i].print("];");
                String command = new String(cmdByteArray[i].toByteArray(), StandardCharsets.UTF_8);
                System.out.println("octave: " + command.substring(0, Math.min(command.length(), 100)));
                eval(command);
            }
        } catch (IOException e) {
        }
    }
