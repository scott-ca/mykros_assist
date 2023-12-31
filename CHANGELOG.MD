# CHANGELOG

All notable improvements, changes, and fixes to Mykros will be documented in this file.

## [Pre-release]


## [0.2.7] - 2023-1-04
### Minor changes

- Minimal set of dialog management was initially being trained on the rasa model, even though it wasn't being used. Since it is only being used for NLU and not any dialog management, it has been updated to be trained only for the NLU portion. This has reduced the ram usage while the model is loaded by Mykros by approximately 10%.

## [0.2.6] - 2023-1-01
### Minor changes

- Resolved an issue where disabled intents could still be detected even though they couldn't be triggered if they shared training data with an enabled intent that uses the same custom action function. Instead of getting the most likely intent for your intent, you may get an error because it would try to process a disable intent.

In most cases, each intent possesses unique custom action functions and training data. When such intents are disabled, their data isn't used to train the model. In those cases you get no error as the model doesn't have any data on how to trigger those intents and thus wouldn't  be able to detect the intent.

As a result of this bugfix, the rare instances where multiple intents share a custom action function and training data, only the enabled intents will now be considered, ensuring both disabled intents and non-existant intents are effectively omitted even if they were present in the training data. Allowing you to instead get the highest confidence score intent versus the error you would previously recieved.

This also means, you can now have someone export intents that share custom action functions and training data without getting an error just because they didn't export all of the intents that use that shared custom action function and training data.


## [0.2.5] - 2023-10-30
### Minor changes

- Added additional functionality to the export and import function. When exporting custom actions, Mykros creates a text file within the zip that lists any required non-standard libraries that were imported in the custom action function, along with their versions from the current environment being run. During import of the custom action, this file is treated as a requirements file, ensuring that the specific versions of these libraries are installed in the enviroment.

- Added the __pycache__ as a folder to not add to the zip when exporting custom_action_functions.

## [0.2.4] - 2023-10-29
### Minor changes

- Added functionality to import and export custom action functions, training data, and intent_config data, respective domain entity data for intents. This can be done with a single intent or multiple intents at the same time. In addition, should there be duplicates of any of the custom action function files or training data you will be prompted to if you want to overwrite it. You will also get a similar prompt if the intent information already exists in the intent_config.yml file and the entity data in the domain file prompting if you wish to overwrite the data.

Currently should the custom action function require any libraries not already installed, you will need to install the missing libraries into the portable conda enviroment manually. However, this functionality is currently being worked on to be automatically done when you import/export custom actions.

- Fixed a bug that caused the enabled(true)/disabled(false) translation setting in the settings.yml file to default to true if an invalid value was detected instead of defaulting to false.

## [0.2.3] - 2023-10-26
### Minor changes

- Added feature to the system tray context menu for custom actions. Once you updated the custom actions function, training data, or enabled/disabled actions you can now re-train the model from this menu as well. It will close Mykros and train the model, once it is complete it will automatically re-launch Mykros.

You can still update all of the data and train the model via the old method, this just allows someone who does it via the GUI to train the model from the UI as well as have it automatically re-launch Mykros.

-- Added the --auto flag to the update_data.py script and will also be passed along should it be launched from update_data.sh(linux) and update_data.bat(windows) should you run them with the --auto flag. In doing so it will auto-accept the prompt to replace any pre-existing models should one be found. 

## [0.2.2] - 2023-10-26
### Major changes

- Added system tray context menu for custom actions. It will display all of the intents, custom actions, descriptions, and if they are enabled. In addition, you hae the option to enable/disable intents/actions as well as edit the custom_actions function and training data from within Mykros. 

You also have the option to backup your changes and restore them as well from your last backup. This should make updating or tweaking your custom actions and the respect training data more streamlined. You no longer need to manually browse to the respective folders and open the files to make the changes, and have a built in way to restore your previous version instead of manually needing to create a backup.

You will still need to re-train your model manually. However, a feature is being worked on to allow you to trigger the re-training of the model from within Mykros. 

## [0.2.1] - 2023-10-25
### Major changes

- Implemented translate_words custom action for translating words and phrases without needing to enable the global setting for input/output.

- We've improved the accuracy for entity detection for recognizing longer, more complex phrases through two enhancements:

**Config/Model changes:** The CRFEntityExtractor was integrated, enhancing the system's capability to recognize longer phrases more effectively. This feature complements the existing featurizers including the DIETClassifier, which remains essential for identifying entities as well as assisting with detection should the input receive typos. In addition the word analyzer was added for the CountVectorsFeaturizer.

**Additional framework entity prioritization:**

The second enhancement added embedded functionality for entity prioritization that assists when multiple featurizers extract data for the same entity. This assists with better phrase detection, but also assists with ensuring correct entity is detection. This only occurs with multiple extractions of the same entity, it doesn't impact which entities are extracted between different entities.

The priority is given to the extraction that the most words within that specific entity. When entities have the same word counts, the system defaults to the one with the highest confidence score. An exception is made for the RegexEntityExtractor. The RegexEntityExtractor takes priorty regardless of the word count due to it being derived from the custom regex patterns you defined specifically for that entity. This prioritization of entities will also integrate with any additional featurizers you may enable in the config file as they are not the specific to just CRFEntityExtractor and DIETClassifier. The only requirement is that featurizer used provides a confidence score for the entity extraction.

- The regex in the training data for run_terminal was incorrect which caused the word terminal to be included in the entity instead of just extracting the text after the word terminal. **Please note*: There is currently an issue on linux with commands that utilize the curses library, this is commonly used for terminal applications that have a dynamic UI(htop/top/nano/vim/etc), that causes Mykros to freeze until those applications and processes are ended. This only impacts those commands, any commands that provide static terminal output will run inside of Mykros without causing an issue.

### Minor changes/Bug fixes

- Developers now have the ability to access the translation functionality for their own custom actions. Once they import the module, they will only need to call the translate_custom function and provide the text to be translated and the 2 character code for the from and to languages. This is separate from the functionality that already existed to translate all input and/or output that the user can enable.

- Should you be working with translations that bypass English and require an intermediate language, for instance, translating from Spanish to Slovak you no longer need to manually change your settings to Spanish->English to download the model and then change it to English->Slovak to download the model. This process is now automatic and will download the required models to use the intermediate languages needed to complete the translation.

- When utilizing translation models, the downloaded zip of the model is no longer stored after it has been extracted. This reduces the disk space used for language models as only the model is stored now.

- Previously when linking multiple actions via using export/input it would occasionally allow too many intents if the intents weren't all part of the same conflict group. It now consider them as if they were part of the conflict group to ensure it allows the correct amount of intents. 

- Added version numbers to better track releases and changes in a more user readable format and to better allow for additioanl context.
 

## [0.2.0] - 2023-10-13

### Major changes

- Introduces comprehensive cross-language support, allowing you to interact with models in other languages. This feature can be configured to be used for only intent detection, all input, all output, or both input and output. This feature provides seamless interaction with the models and the custom_actions without needing to do any additional configuration to support the feature as it's native to the framework. 

- Implemented a convert_units custom action for converting between various measurments. The custom action supports various types of measurements including length, mass, time, temperature, volume, frequency, and more. This is run locally and doesn't connect to the internet to perform the operation.

### Minor changes/Bug fixes

- Added the __DASH__ placeholder and the relevant documentation for that placeholder as well as the other pre-existing placeholders to used in training data.

- Improved accuracy of the check_spelling custom action.

## [0.1.0] - 2023-09-29
- Initial pre-release version of Mykros, laying the foundation for the AI assistant and the framework. This version introduces the core functionalities and establishes the groundwork for future enhancements and features.