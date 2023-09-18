import os
import subprocess
import json5
import json
import requests
import shutil
import re
import base64

from tqdm import tqdm


# Constants
manifest = "manifest.json"
minecraft_instance_file = "minecraftinstance.json"
overrides_folder = "overrides"
secrets_file = "secrets.jsonc"
settings_file = "settings.jsonc"

instance_root = os.getcwd()

# Secrets
try:
    # Read the JSON file
    with open(settings_file, "r") as json_file, open(secrets_file, "r") as json_file1:
        json_data = json5.load(json_file)
        json_data1 = json5.load(json_file1)
    # Now, json_data contains the contents of settings.json as a parsed dictionary
    print("JSON data loaded successfully:")
except:
    try:
        with open(secrets_file, "r") as json_file:
            file_size = os.path.getsize(secrets_file)
            if file_size == 0:
                dataSecrets = """{
        // CURSEFORGE ACCOUNT SETTINGS
        // CURSEFORGE UPLOAD API
        // Get one here: https://curseforge.com/account/api-tokens
        "CURSEFORGE_UPLOAD_TOKEN": "My-Token",
        // GITHUB COMPATIBILITY SETTINGS
        // Example for this repo:
        // https://github.com/$GITHUB_NAME/$GITHUB_REPOSITORY
        "GITHUB_NAME": "MyGitHubUsername",
        "GITHUB_REPOSITORY": "MyModpack",
        "GITHUB_TOKEN": "MyGitHubUsername:MY-SECRET-GITHUB-TOKEN"
    }"""
                # Write the contents to the file as JSON
                with open(secrets_file, 'w') as json_file1:
                    json_file1.write(dataSecrets)
    
        with open(settings_file, "r") as json_file:
                    file_size = os.path.getsize(settings_file)
                    if file_size == 0:
                        data = """{
    // =====================================================================//
    //  CURSEFORGE ACCOUNT SETTINGS
    // =====================================================================//
    
    "CURSEFORGE_AUTHOR": "JohnDoe",
    
    // ProjectID can be found on the modpack's Curseforge Projects page, under "About This Project"
    "CF_ID": 123456,
    
    // =====================================================================//
    //  MAIN MODPACK SETTINGS
    // =====================================================================//
    
    // This is the modpack name as seen on the CurseForge page
    "MODPACK_NAME": "MyModpack",
    
    // Name of the Modpack in the ZIP File
    "CLIENT_NAME": "MyModpack",
    
    // Version Of The Modpack
    "MODPACK_VERSION": "1.0.1",
    
    // Last Version Of The Modpack
    // Needed For Changelog Parsing
    // Should be "null" if this is the first release
    "LAST_MODPACK_VERSION": "1.0.0",
    
    // Which modloader the modpack uses
    // Can be "forge" or "fabric"
    // Default: "forge"
    "MODLOADER": "forge",
    
    // =====================================================================//
    //  CURSEFORGE PROJECT SETTINGS
    // =====================================================================//
    
    // Modpack's Minecraft Version
    // 4449 - 1.7.10
    // 5806 - 1.8.9
    // 6084 - 1.9.4
    // 6170 - 1.10.2
    // 6452 - 1.11.2
    // 6756 - 1.12.2
    // 7132 - 1.13.2
    // 7469 - 1.14.4
    // 7722 - 1.15.2
    // 8203 - 1.16.5
    // 9008 - 1.18.2
    "GAME_VERSIONS": [0],
    
    // Can be "alpha", "beta" or "release"
    "RELEASE_TYPE": "release",
    
    //=====================================================================//
    //  CLIENT FILE SETTINGS
    //=====================================================================//
    // Note: "mods" is included automatically and will break the script if you include it yourself.
    "FOLDERS_TO_INCLUDE_IN_CLIENT_FILES": [
        "config",
        "defaultconfigs",
        "kubejs"
    ],
        
    // Example: "Apotheosis-1.19.2-6.2.1.jar", "create-1.19.2-0.5.1.b.jar"
    "FILES_TO_INCLUDE_IN_MODS_FOLDER_IN_CLIENT_FILES": [],
    
    //=====================================================================//
    //  SERVER FILE SETTINGS
    //=====================================================================//
    
    "SERVER_FILES_FOLDER": "server_files",

    // This is in addition to the files already in $
    "FOLDERS_TO_INCLUDE_IN_SERVER_FILES": [
        "config",
        "defaultconfigs",
        "kubejs"
    ],

    // =====================================================================//
    //  MODULES
    // =====================================================================//
    
    // Toggle automatic building of the manifest zip on/off
    // Default: true
    "ENABLE_CLIENT_FILE_MODULE": true,
    
    // Toggle the modpack uploader on/off
    // Setting this to false will also disable the Server File and Changelog Generator Modules.
    // Default: true
    "ENABLE_MODPACK_UPLOADER_MODULE": true,
    
    // Toggle server file feature on/off
    // Default: true
    "ENABLE_SERVER_FILE_MODULE": true,
    
    // Toggle automatic changelog generator on/off
    // This module requires an older modpack manifest zip to be present, 
    // LAST_MODPACK_VERSION must be set, and the manifest naming must be consistent.
    // Default: false
    "ENABLE_CHANGELOG_GENERATOR_MODULE": false,
    
    // Path to the ChangelogGenerator's output file
    "CHANGELOG_PATH": "INSTANCE_ROOT/changelogs/changelog_mods_MODPACK_VERSION.md",
    
    // Toggle creation of a modlist file on/off
    // Default: true
    "ENABLE_MODLIST_CREATOR_MODULE": true,
    // Path to the ModListCreator's output file
    "MODLIST_PATH": "INSTANCE_ROOT/changelogs/modlist_MODPACK_VERSION.md",
    
    // Toggle removal and re-download of jars on/off.
    // Setting this to true will ensure that you always have the latest 
    // Twitch Export Builder and ChangelogGenerator, but increases the
    // amount of time this script takes to execute.
    // Default: false
    "ENABLE_ALWAYS_UPDATE_JARS": false,
    
    // Toggles github release integration on/off.
    // This will create a new release on your issue-tracker when using the modpack uploader.
    // See below link for info:
    // Default: false
    "ENABLE_GITHUB_RELEASE_MODULE": false
}"""
                        # Write the contents to the file as JSON
                        with open(settings_file, 'w') as json_file:
                            json_file.write(data)
    except:
        try:
            with open(settings_file, "r") as json_file:
                file_size = os.path.getsize(settings_file)
        except:
            data = """{
    // =====================================================================//
    //  CURSEFORGE ACCOUNT SETTINGS
    // =====================================================================//
    
    "CURSEFORGE_AUTHOR": "JohnDoe",
    
    // ProjectID can be found on the modpack's Curseforge Projects page, under "About This Project"
    "CF_ID": 123456,
    
    // =====================================================================//
    //  MAIN MODPACK SETTINGS
    // =====================================================================//
    
    // This is the modpack name as seen on the CurseForge page
    "MODPACK_NAME": "MyModpack",
    
    // Name of the Modpack in the ZIP File
    "CLIENT_NAME": "MyModpack",
    
    // Version Of The Modpack
    "MODPACK_VERSION": "1.0.1",
    
    // Last Version Of The Modpack
    // Needed For Changelog Parsing
    // Should be "null" if this is the first release
    "LAST_MODPACK_VERSION": "1.0.0",
    
    // Which modloader the modpack uses
    // Can be "forge" or "fabric"
    // Default: "forge"
    "MODLOADER": "forge",
    
    // =====================================================================//
    //  CURSEFORGE PROJECT SETTINGS
    // =====================================================================//
    
    // Modpack's Minecraft Version
    // 4449 - 1.7.10
    // 5806 - 1.8.9
    // 6084 - 1.9.4
    // 6170 - 1.10.2
    // 6452 - 1.11.2
    // 6756 - 1.12.2
    // 7132 - 1.13.2
    // 7469 - 1.14.4
    // 7722 - 1.15.2
    // 8203 - 1.16.5
    // 9008 - 1.18.2
    "GAME_VERSIONS": [0],
    
    // Can be "alpha", "beta" or "release"
    "RELEASE_TYPE": "release",
    
    //=====================================================================//
    //  CLIENT FILE SETTINGS
    //=====================================================================//
    // Note: "mods" is included automatically and will break the script if you include it yourself.
    "FOLDERS_TO_INCLUDE_IN_CLIENT_FILES": [
        "config",
        "defaultconfigs",
        "kubejs"
    ],
        
    // Example: "Apotheosis-1.19.2-6.2.1.jar", "create-1.19.2-0.5.1.b.jar"
    "FILES_TO_INCLUDE_IN_MODS_FOLDER_IN_CLIENT_FILES": [],
    
    //=====================================================================//
    //  SERVER FILE SETTINGS
    //=====================================================================//
    
    "SERVER_FILES_FOLDER": "server_files",

    // This is in addition to the files already in $
    "FOLDERS_TO_INCLUDE_IN_SERVER_FILES": [
        "config",
        "defaultconfigs",
        "kubejs"
    ],
   
    // =====================================================================//
    //  MODULES
    // =====================================================================//
    
    // Toggle automatic building of the manifest zip on/off
    // Default: true
    "ENABLE_CLIENT_FILE_MODULE": true,
    
    // Toggle the modpack uploader on/off
    // Setting this to false will also disable the Server File and Changelog Generator Modules.
    // Default: true
    "ENABLE_MODPACK_UPLOADER_MODULE": true,
    
    // Toggle server file feature on/off
    // Default: true
    "ENABLE_SERVER_FILE_MODULE": true,
    
    // Toggle automatic changelog generator on/off
    // This module requires an older modpack manifest zip to be present, 
    // LAST_MODPACK_VERSION must be set, and the manifest naming must be consistent.
    // Default: false
    "ENABLE_CHANGELOG_GENERATOR_MODULE": false,
    // Path to the ChangelogGenerator's output file
    "CHANGELOG_PATH": "INSTANCE_ROOT/changelogs/changelog_mods_MODPACK_VERSION.md",
    
    // Toggle creation of a modlist file on/off
    // Default: true
    "ENABLE_MODLIST_CREATOR_MODULE": true,
    // Path to the ModListCreator's output file
    "MODLIST_PATH": "INSTANCE_ROOT/changelogs/modlist_MODPACK_VERSION.md",
    
    // Toggle removal and re-download of jars on/off.
    // Setting this to true will ensure that you always have the latest 
    // Twitch Export Builder and ChangelogGenerator, but increases the
    // amount of time this script takes to execute.
    // Default: false
    "ENABLE_ALWAYS_UPDATE_JARS": false,
    
    // Toggles github release integration on/off.
    // This will create a new release on your issue-tracker when using the modpack uploader.
    // See below link for info:
    // Default: false
    "ENABLE_GITHUB_RELEASE_MODULE": false
}"""
            # Write the contents to the file as JSON
            with open(settings_file, 'w') as json_file:
                json_file.write(data)
                try:
                    with open(secrets_file, "r") as json_file:
                        hello = "world"
                except:   
                    dataSecrets = """{
    // CURSEFORGE ACCOUNT SETTINGS
    // CURSEFORGE UPLOAD API
    // Get one here: https://curseforge.com/account/api-tokens
    "CURSEFORGE_UPLOAD_TOKEN": "My-Token",
    // GITHUB COMPATIBILITY SETTINGS
    // Example for this repo:
    // https://github.com/$GITHUB_NAME/$GITHUB_REPOSITORY
    "GITHUB_NAME": "MyGitHubUsername",
    "GITHUB_REPOSITORY": "MyModpack",
    "GITHUB_TOKEN": "MyGitHubUsername:MY-SECRET-GITHUB-TOKEN"
}"""
                    # Write the contents to the file as JSON
                    with open(secrets_file, 'w') as json_file1:
                        json_file1.write(dataSecrets)


try:
    with open(secrets_file, "r") as file:
        file_size = os.path.getsize(secrets_file)
        if file_size == 0:
            world = "hello"
except:
    winStart1 = dataSecrets = """{
    // CURSEFORGE ACCOUNT SETTINGS
    // CURSEFORGE UPLOAD API
    // Get one here: https://curseforge.com/account/api-tokens
    "CURSEFORGE_UPLOAD_TOKEN": "My-Token",
    // GITHUB COMPATIBILITY SETTINGS
    // Example for this repo:
    // https://github.com/$GITHUB_NAME/$GITHUB_REPOSITORY
    "GITHUB_NAME": "MyGitHubUsername",
    "GITHUB_REPOSITORY": "MyModpack",
    "GITHUB_TOKEN": "MyGitHubUsername:MY-SECRET-GITHUB-TOKEN"
}"""
    # Write the contents to the file as JSON
    with open(secrets_file, 'w') as json_file1:
        json_file1.write(dataSecrets)

# ADVANCED SETTINGS
CLIENT_ZIP_NAME = json_data.get("CLIENT_NAME") + "-" + json_data.get("MODPACK_VERSION")
LAST_CLIENT_ZIP_NAME = json_data.get("CLIENT_NAME") + "-" + json_data.get("LAST_MODPACK_VERSION")
CLIENT_FILE_DISPLAY_NAME = json_data.get("CLIENT_NAME") + " " + json_data.get("MODPACK_VERSION")
SERVER_FILE_DISPLAY_NAME = "[Server Files] " + json_data.get("CLIENT_NAME") + " " + json_data.get("MODPACK_VERSION")
SERVER_ZIP_NAME = json_data.get("CLIENT_NAME") + "-" + "Server" + "-" + json_data.get("MODPACK_VERSION")
CF_ID = json_data.get("CURSEFORGE_PROJECT_ID")
CURSEFORGE_AUTHOR = json_data.get("CURSEFORGE_AUTHOR")
CURSEFORGE_UPLOAD_TOKEN = json_data1.get("CURSEFORGE_UPLOAD_TOKEN")
SERVER_FILES_FOLDER = json_data.get("SERVER_FILES_FOLDER")

if json_data.get("ENABLE_SERVER_FILE_MODULE") == True:
    try:
        os.mkdir(json_data.get("SERVER_FILES_FOLDER"))
    except:
        pass
    try:
        with open(json_data.get("SERVER_FILES_FOLDER") + "/start-server.bat", "r") as file:
            hello = "world"
    except:
        winStart1 = """@ECHO OFF
SETLOCAL


:BEGIN
CLS
COLOR 3F >nul 2>&1
SET MC_SYS32=%SYSTEMROOT%\SYSTEM32
REM Make batch directory the same as the directory it's being called from
REM For example, if "run as admin" the batch starting dir could be system32
CD "%~dp0" >nul 2>&1

:CHECK
REM Check if serverstarter JAR is already downloaded
IF NOT EXIST "%cd%\serverstarter-2.4.0.jar" (
	ECHO serverstarter binary not found, downloading serverstarter...
	%SYSTEMROOT%\SYSTEM32\bitsadmin.exe /rawreturn /nowrap /transfer starter /dynamic /download /priority foreground cdn.naylahanegan.com/serverstarter-2.4.0.jar "%cd%\serverstarter-2.4.0.jar"
   GOTO MAIN
) ELSE (
   GOTO MAIN
)

:MAIN
java -jar serverstarter-2.4.0.jar
GOTO EOF

:EOF
pause"""
        # Write the contents to the file
        with open(json_data.get("SERVER_FILES_FOLDER") + "/start-server.bat", "w") as file:
            file.write(winStart1)
    try:
        with open(json_data.get("SERVER_FILES_FOLDER") + "/start-server.sh", "r") as file:
            hello = "World"
    except:
        linStart1 = """#!/bin/bash
DO_RAMDISK=0
if [[ $(cat server-setup-config.yaml | grep 'ramDisk:' | awk 'BEGIN {FS=":"}{print $2}') =~ "yes" ]]; then
    SAVE_DIR=$(cat server.properties | grep 'level-name' | awk 'BEGIN {FS="="}{print $2}')
    mv "$SAVE_DIR" "${SAVE_DIR}_backup"
    mkdir "$SAVE_DIR"
    sudo mount -t tmpfs -o size=2G tmpfs "$SAVE_DIR"
    DO_RAMDISK=1
fi
if [ -f serverstarter-2.2.0.jar ]; then
    echo "Skipping download. Using existing serverstarter-2.2.0.jar"
    java -jar serverstarter-2.2.0.jar
    if [[ $DO_RAMDISK -eq 1 ]]; then
        sudo umount "$SAVE_DIR"
        rm -rf "$SAVE_DIR"
        mv "${SAVE_DIR}_backup" "$SAVE_DIR"
    fi
    exit 0
else
    export URL="cdn.naylahanegan.com/serverstarter-2.4.0.jar"
fi
echo $URL
if command -v wget >>/dev/null; then
    echo "DEBUG: (wget) Downloading ${URL}"
    wget -O serverstarter-2.2.0.jar "${URL}"
else
    if command -v curl >>/dev/null; then
        echo "DEBUG: (curl) Downloading ${URL}"
        curl -L -o serverstarter-2.2.0.jar "${URL}"
    else
        echo "Neither wget or curl were found on your system. Please install one and try again"
    fi
fi
java -jar serverstarter-2.2.0.jar
if [[ $DO_RAMDISK -eq 1 ]]; then
    sudo umount "$SAVE_DIR"
    rm -rf "$SAVE_DIR"
    mv "${SAVE_DIR}_backup" "$SAVE_DIR"
fi"""
        # Write the contents to the file
        with open(json_data.get("SERVER_FILES_FOLDER") + "/start-server.sh", "w") as file:
            file.write(linStart1)
try:
    with open(json_data.get("SERVER_FILES_FOLDER") + "/server-setup-config.yaml", "r") as file:
        hello = "World"
except:
    serverF = """# Version of the specs, only for internal usage if this format should ever change drastically
_specver: 2

# modpack related settings, changes the supposed to change the visual appearance of the launcher
modpack:
  # Name of the mod pack, that is displayed in various places where it fits
  name: Example Modpack

  # Description
  description: This is a awesome modpack about making examples.



# settings regarding the installation of the modpack
install:
  # version of minecraft, needs the exact version
  mcVersion: 1.17.1

  # exact version of forge or fabric that is supposed to be used
  # if this value is a null value so ( ~, null, or "" ) then the version from the mod pack is going to be used
  loaderVersion: 37.0.95

  # If a custom installer is supposed to used, specify the url here: (Otherwise put "", ~ or null here)
  # supports variables: {{@loaderversion@}} and {{@mcversion@}}
  # For forge: "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{{@mcversion@}}-{{@loaderversion@}}/forge-{{@mcversion@}}-{{@loaderversion@}}-installer.jar"
  # For Fabric: "https://maven.fabricmc.net/net/fabricmc/fabric-installer/{{@loaderversion@}}/fabric-installer-{{@loaderversion@}}.jar"
  installerUrl: "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{{@mcversion@}}-{{@loaderversion@}}/forge-{{@mcversion@}}-{{@loaderversion@}}-installer.jar"

  # Installer Arguments
  # These Arguments have to be passed to the installer
  #
  # For Fabric:
  # installerArguments:
  #   - "-downloadMinecraft"
  #   - "server"
  #
  # For Forge:
  # installerArguments:
  #   - "--installServer"
  installerArguments:
    - "--installServer"

  # Link to where the file where the modpack can be distributed
  # This supports loading from local files as well for most pack types if there is file://{PathToFile} in the beginning
  modpackUrl: https://media.forgecdn.net/files/3491/186/All+the+Mods+7-0.0.21.zip

  # This is used to specify in which format the modpack is distributed, the server launcher has to handle each individually if their format differs
  # current supported formats:
  # - curseforge or curse
  # - curseid
  # - zip or zipfile
  modpackFormat: curse

  # Settings which are specific to the format used, might not be needed in some casese
  formatSpecific:
    # optional paramenter used for curse to specify a whole project to ignore (mostly if it is client side only)
    ignoreProject:
      - 263420
      - 317780
      - 232131
      - 231275
      - 367706
      - 261725
      - 243863
      - 305373
      - 325492
      - 296468
      - 308240
      - 362791
      - 291788
      - 326950
      - 237701
      - 391382
      - 358191
      - 271740
      - 428199
      - 431430

  # The base path where the server should be installed to, ~ for current path
  baseInstallPath: setup/

  # a list of files which are supposed to be ignored when installing it from the client files
  # this can either use regex or glob {default glob: https://docs.oracle.com/javase/8/docs/api/java/nio/file/FileSystem.html#getPathMatcher-java.lang.String-}
  # specify with regex:.... or glob:.... if you want to force a matching type
  ignoreFiles:
    - mods/Overrides.txt
    - mods/optifine*.jar
    - mods/optiforge*.jar
    - resources/**
    - packmenu/**
    - openloader/resources/**

  # often a server needs more files, which are nearly useless on the client, such as tickprofiler
  # This is a list of files, each ' - ' is a new file:
  # url is the directlink to the file, destination is the path to where the file should be copied to
  additionalFiles: ~
    #- url: https://media.forgecdn.net/files/2844/278/restrictedportals-1.15-1.0.jar
    #  destination: mods/restrictedportals-1.15-1.0.jar
    #- url: https://media.forgecdn.net/files/2874/966/Morpheus-1.15.2-4.2.46.jar
    #  destination: mods/Morpheus-1.15.2-4.2.46.jar
    #- url: https://media.forgecdn.net/files/2876/89/spark-forge.jar
    #  destination: mods/spark-forge.jar

  # For often there are config which the user wants to change, here is the place to put the local path to configs, jars or whatever
  # You can copy files or folders
  localFiles:
    - from: setup/modpack-download.zip
      to: setup/test/modpack-download-copied.zip
    - from: setup/AOF 2/.minecraft
      to: setup/.

  # This makes the program check the folder for whether it is supposed to use the
  checkFolder: true

  # Whether to install the Loader (Forge or Fabric) or not, should always be true unless you only want to install the pack
  installLoader: true

  # Whether to install the Pack from supplied link or zipfile or just run an already installed pack
  # Will download mods from manifest or minecraftinstance.json depending on modpackformat
  installPack: true

  # Sponge bootstrapper jar URL
  # Only needed if you have spongefix enabled
  spongeBootstrapper: https://github.com/simon816/SpongeBootstrap/releases/download/v0.7.1/SpongeBootstrap-0.7.1.jar

  # Time in seconds before the connection attempt to any webservice like forge/curseforge times out
  # Only increase this timer if you have problems
  connectTimeout: 30

  # Time in seconds before the read attempt to any webservice like forge/curseforge times out
  # Only increase this timer if you have problems
  readTimeout: 30



# settings regarding the launching of the pack
launch:
  # applies the launch wrapper to fix sponge for a few mods
  spongefix: false

  # Use a RAMDisk for the world folder
  # case-sensitive; use only lowercase `true` or `false`
  # NOTE: The server must have run once fully before switching to `true`!
  ramDisk: false

  # checks with the help of a few unrelated server whether the server is online
  checkOffline: true

  # specifies the max amount of ram the server is supposed to launch with
  maxRam: 5G

  # specifies the min amount of ram the server is supposed to launch with
  minRam: 2G

  # specifies whether the server is supposed to auto restart after crash
  autoRestart: true

  # after a given amount of crashes in a given time the server will stop auto restarting
  crashLimit: 10

  # Time a crash should be still accounted for in the {crashLimit}
  # syntax is either [number]h or [number]min or [number]s
  crashTimer: 60min

  # Arguments that need to go before the 'java' argument, something like linux niceness
  # This is only a string, not a list.
  preJavaArgs: ~

  # Start File Name, variables: {{@loaderversion@}} and {{@mcversion@}}
  # This has to be the name the installer spits out
  # For Forge 1.12-: "forge-{{@mcversion@}}-{{@loaderversion@}}-universal.jar"
  # For Forge 1.13+: "forge-{{@mcversion@}}-{{@loaderversion@}}.jar"
  # For Fabric: "fabric-server-launch.jar"
  startFile: "forge-{{@mcversion@}}-{{@loaderversion@}}.jar"

  # This is the command how the server is supposed to be started
  # For <1.16 it should be
  #  - "-jar"
  #  - "{{@startFile@}}"
  #  - "nogui"
  # For >=1.17 it should be
  # - "@libraries/net/minecraftforge/forge/{{@mcversion@}}-{{@loaderversion@}}/{{@os@}}_args.txt"
  # - "nogui"
  startCommand:
    - "@libraries/net/minecraftforge/forge/{{@mcversion@}}-{{@loaderversion@}}/{{@os@}}_args.txt"
    - "nogui"

  # In case you have multiple javas installed you can add a absolute path to it here
  # The Path has to be enclosed in \" like in the example if it has spaces (or for safety just include them always.)
  # if the value is "", null, or ~ then 'java' from PATH is going to be used
  # Example: "\"C:/Program Files/Java/jre1.8.0_201/bin/java.exe\""
  # It also supports replacing with environment variables with ${ENV_VAR} e.g. ${JAVA_HOME}/bin/java.exe
  forcedJavaPath: ~

  # Java args that are supposed to be used when the server launches
  # keep in mind java args often need ' - ' in front of it to work, use clarifying parentheses to make sure it uses it correctly
  # Keep in mind that some arguments only work on JRE 1.8
  # reference: https://aikar.co/2018/07/02/tuning-the-jvm-g1gc-garbage-collector-flags-for-minecraft/
  javaArgs:
    - "-XX:+UseG1GC"
    - "-XX:+ParallelRefProcEnabled"
    - "-XX:MaxGCPauseMillis=200"
    - "-XX:+UnlockExperimentalVMOptions"
    - "-XX:+DisableExplicitGC"
    - "-XX:+AlwaysPreTouch"
    - "-XX:G1NewSizePercent=30"
    - "-XX:G1MaxNewSizePercent=40"
    - "-XX:G1HeapRegionSize=8M"
    - "-XX:G1ReservePercent=20"
    - "-XX:G1HeapWastePercent=5"
    - "-XX:G1MixedGCCountTarget=4"
    - "-XX:InitiatingHeapOccupancyPercent=15"
    - "-XX:G1MixedGCLiveThresholdPercent=90"
    - "-XX:G1RSetUpdatingPauseTimePercent=5"
    - "-XX:SurvivorRatio=32"
    - "-XX:+PerfDisableSharedMem"
    - "-XX:MaxTenuringThreshold=1"
    - "-Dfml.readTimeout=90"                        # servertimeout
    - "-Dfml.queryResult=confirm"                   # auto /fmlconfirm"""
    # Write the contents to the file
    with open(json_data.get("SERVER_FILES_FOLDER") + "/server-setup-config.yaml", "w") as file:
        file.write(serverF)

try:
    with open(secrets_file, "r") as json_file2:
        hello = "world"
except:
    dataSecrets = """{
    // CURSEFORGE ACCOUNT SETTINGS
    // CURSEFORGE UPLOAD API
    // Get one here: https://curseforge.com/account/api-tokens
    "CURSEFORGE_UPLOAD_TOKEN": "My-Token",
    // GITHUB COMPATIBILITY SETTINGS
    // Example for this repo:
    // https://github.com/$GITHUB_NAME/$GITHUB_REPOSITORY
    "GITHUB_NAME": "MyGitHubUsername",
    "GITHUB_REPOSITORY": "MyModpack",
    "GITHUB_TOKEN": "MyGitHubUsername:MY-SECRET-GITHUB-TOKEN"
}"""
    with open(secrets_file, "w") as json_file2:
        json_file2.write(dataSecrets)


# Function to test for dependencies
def test_for_dependencies():
    is_7z_available = shutil.which("7z")
    
    if not is_7z_available:
        print("Install 7zip and add its folder to the environment variable 'Path'")
        print("7zip can be downloaded here: https://www.7-zip.org/download.html")
        print("When you're done, rerun this script.")
        raise Exception("7zip not command available. Please follow the instructions above.")
    
    is_curl_available = shutil.which("curl")
    
    if not is_curl_available:
        print("Install Curl and add its folder to the environment variable 'Path'")
        print("Curl can be downloaded here: https://curl.se/download.html")
        print("To install it, simply unzip the folder somewhere and add it to your system's PATH.")
        print("When you're done, rerun this script.")
        raise Exception("Curl not available. Please follow the instructions above.")


# Function to create client files
def new_client_files():
    if json_data.get("ENABLE_CLIENT_FILE_MODULE") is True:
        print("Creating Client Files...")
        
        client_zip = f"{CLIENT_ZIP_NAME}.zip"
        if os.path.exists(client_zip):
            os.remove(client_zip)
        
        shutil.rmtree(overrides_folder, ignore_errors=True)
        os.makedirs(overrides_folder)
        
        for folder in json_data.get("FOLDERS_TO_INCLUDE_IN_CLIENT_FILES"):
            print(f"Adding {folder} to client files.")
            destination_folder = os.path.join(overrides_folder, folder)
            
            if not os.path.exists(destination_folder):
                shutil.copytree(folder, destination_folder)
        
        destination_folder = os.path.join(overrides_folder, "mods")
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        for file in json_data.get("FILES_TO_INCLUDE_IN_MODS_FOLDER_IN_CLIENT_FILES", []):
            print(f"Adding {file} to the mods folder in the client files.")
            shutil.copy(file, os.path.join("mods/" + destination_folder, os.path.basename(file)))
        
        remove_blacklisted_files()

        new_manifest_json()

        # Zipping up the newly created overrides folder and manifest
        subprocess.run(["7z", "a", client_zip, overrides_folder, manifest, "-r", "-sdel"], check=True)
        
        if os.path.exists(manifest):
            os.remove(manifest)

        print(f"Client files {client_zip} created!")

# Function to create a manifest JSON
def new_manifest_json():
    if not os.path.exists(minecraft_instance_file):
        print(f"Generating a {manifest} requires a {minecraft_instance_file} file.")
        return
    
    with open(minecraft_instance_file, "r", encoding='utf-8') as file: # Stupid CurseForge encoding
        minecraft_instance_json = json.load(file)
    
    mods = []
    for addon in minecraft_instance_json["installedAddons"]:
        mods.append({
            "required": True,
            "projectID": addon["addonID"],
            "fileID": addon["installedFile"]["id"],
            "downloadUrl": addon["installedFile"]["downloadUrl"]
        })
    
    modloader_id = minecraft_instance_json["baseModLoader"]["name"]
    
    if json_data.get("MODLOADER") == "fabric":
        split_modloader_id = modloader_id.split("-")
        modloader_id = "-".join(split_modloader_id[:2])
    
    json_output = {
        "minecraft": {
            "version": minecraft_instance_json["baseModLoader"]["minecraftVersion"],
            "modLoaders": [
                {
                    "id": modloader_id,
                    "primary": True
                }
            ]
        },
        "manifestType": "minecraftModpack",
        "manifestVersion": 1,
        "name": json_data.get("MODPACK_NAME"),
        "version": json_data.get("MODPACK_VERSION"),
        "author": json_data.get("CURSEFORGE_AUTHOR"),
        "files": mods,
        "overrides": overrides_folder
    }
    
    if os.path.exists(manifest):
        os.remove(manifest)
    
    with open(manifest, "w") as file:
        json.dump(json_output, file, indent=3)
    
    print(f"{manifest} created!")

# Function to remove blacklisted files
def remove_blacklisted_files():
    if json_data.get("ENABLE_CLIENT_FILE_MODULE") is True or json_data.get("ENABLE_SERVER_FILE_MODULE") is True:
        print("Removing all .bak files from overrides")
        try:
            for file in os.listdir(overrides_folder):
                if file.endswith(".bak"):
                    print(f"Removing {file}")
                    os.remove(os.path.join(overrides_folder, file))
        except:
            pass

# Function to create a changelog
def new_changelog():
    if json_data.get("ENABLE_CHANGELOG_GENERATOR_MODULE") == True and json_data.get("LAST_MODPACK_VERSION") and os.path.exists(f"{instance_root}/{LAST_CLIENT_ZIP_NAME}.zip") and os.path.exists(f"{instance_root}/{CLIENT_ZIP_NAME}.zip"):
        if not os.path.exists(json_data.get("CHANGELOG_MODLIST_GENERATOR_JAR")) or json_data.get("ENABLE_ALWAYS_UPDATE_JARS"):
            if os.path.exists(json_data.get("CHANGELOG_MODLIST_GENERATOR_JAR")):
                os.remove(json_data.get("CHANGELOG_MODLIST_GENERATOR_JAR"))
                r = requests.get("https://cdn.naylahanegan.com/ModListCreator-4.1.0-fatjar.jar")
                file_path = os.path.join(".ModpackSuite", "sModListCreator-4.1.0-fatjar.jar")
                with open(file_path, "wb") as file:
                    file.write(r.content)

        
        print("Generating mod changelog...")
        
        try:
            os.remove(CHANGELOG_PATH)
        except FileNotFoundError:
            pass
        
        subprocess.run(["java", "-jar", CHANGELOG_MODLIST_GENERATOR_JAR, "changelog", "--output", CHANGELOG_PATH, "--new", f"{CLIENT_ZIP_NAME}.zip", "--old", f"{LAST_CLIENT_ZIP_NAME}.zip"], check=True)
        
        print("Mod changelog generated!")

# Function to push client files to CurseForge
def push_client_files():
    if json_data.get("ENABLE_MODPACK_UPLOADER_MODULE") == True:
        remove_blacklisted_files()
        
        CLIENT_METADATA = {
            "changelog": "", # this has to be manual for now. Sorry :()
            "changelogType": "markdown",
            "displayName": CLIENT_FILE_DISPLAY_NAME,
            "gameVersions": json_data.get("GAME_VERSIONS"),
            "releaseType": json_data.get("RELEASE_TYPE")
        }
        
        print("Client Metadata:")
        print(json.dumps(CLIENT_METADATA, indent=3))
        
        print(f"Uploading client files to https://minecraft.curseforge.com/api/projects/{CF_ID}/upload-file")

        headers = {
            "X-Api-Token": CURSEFORGE_UPLOAD_TOKEN,
            "Accept": "application/json",
            "Authorization": f"Basic {base64.b64encode(f'{CURSEFORGE_AUTHOR}:{CURSEFORGE_UPLOAD_TOKEN}'.encode()).decode()}"

        }

        files = {
            "metadata": (None, json.dumps(CLIENT_METADATA)),
            "file": CLIENT_ZIP_NAME + ".zip"
        }
        
        # Make the POST request with a progress bar
        responce = requests.post(f"https://minecraft.curseforge.com/api/projects/{CF_ID}/upload-file", files=files, headers=headers)
        response_json = responce.json()
        client_file_return_id = response_json.get("id")
        if not client_file_return_id:
            print(f"Failed to upload client files: {response_json}")
            raise Exception(f"Failed to upload client files: {response_json}")
        print("Uploaded modpack!")
        print(f"Return Id: {client_file_return_id}")
 
    if json_data.get("ENABLE_SERVER_FILE_MODULE") == True:
        update_file_link_in_server_files(client_file_return_id)


# Function to update file link in server files
def update_file_link_in_server_files(client_file_return_id):
    if client_file_return_id:
        client_file_id_string = str(client_file_return_id)
        id_part1 = str(int(client_file_id_string[:4]))
        id_part2 = str(int(client_file_id_string[4:]))
        
        sanitized_client_zip_name = CLIENT_ZIP_NAME.replace(" ", "+")
        curseforge_cdn_url = f"https://media.forgecdn.net/files/{id_part1}/{id_part2}/{sanitized_client_zip_name}.zip"
        
        with open(json_data.get("SERVER_FILES_FOLDER") + "/server-setup-config.yaml", "r") as file:
            content = file.read()
            content = re.sub(r"https://media.forgecdn.net/files/\d+/\d+/.+.zip", curseforge_cdn_url, content)
        
        with open(json_data.get("SERVER_FILES_FOLDER") + "/server-setup-config.yaml", "w") as file:
            file.write(content)
        
    new_server_files(client_file_return_id)

# Function to create server files
def new_server_files(client_file_return_id):
    server_zip = f"{SERVER_ZIP_NAME}.zip"
    if os.path.exists(server_zip):
        os.remove(server_zip)
    try:
        os.mkdir("tmp")
    except:
        pass
    
    for folder in json_data.get("FOLDERS_TO_INCLUDE_IN_SERVER_FILES"):
        print(f"Adding {folder} to client files.")
        destination_folder = os.path.join(SERVER_FILES_FOLDER, folder)
        
        if not os.path.exists(destination_folder):
            shutil.copytree(folder, destination_folder)
        
        destination_folder = os.path.join(SERVER_FILES_FOLDER, "mods")
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        for file in json_data.get("FILES_TO_INCLUDE_IN_MODS_FOLDER_IN_CLIENT_FILES", []):
            print(f"Adding {file} to the mods folder in the client files.")
            shutil.copy(file, os.path.join("mods/" + destination_folder, os.path.basename(file)))

        subprocess.run(["7z", "a", "-tzip", server_zip, SERVER_FILES_FOLDER + "/*",  "-r", "-sdel"])
        print("Server files created!")
    
    if json_data.get("ENABLE_MODPACK_UPLOADER_MODULE") == True:
        push_server_files(client_file_return_id)

# Function to push server files to CurseForge
def push_server_files(client_file_return_id):
    if json_data.get("ENABLE_SERVER_FILE_MODULE") == True and json_data.get("ENABLE_MODPACK_UPLOADER_MODULE") == True:
        server_file_path = f"{SERVER_ZIP_NAME}.zip"
        
        SERVER_METADATA = {
            "changelog": "", # this has to be manual for now. Sorry :()
            "changelogType": "markdown",
            "displayName": SERVER_FILE_DISPLAY_NAME,
            "parentFileId": client_file_return_id,
            "releaseType": json_data.get("RELEASE_TYPE")
        }
        
        print("Uploading server files...")
        
        headers = {
            "X-Api-Token": CURSEFORGE_UPLOAD_TOKEN,
            "Accept": "application/json",
            "Authorization": f"Basic {base64.b64encode(f'{CURSEFORGE_AUTHOR}:{CURSEFORGE_UPLOAD_TOKEN}'.encode()).decode()}"

        }

        files = {
            "metadata": (None, json.dumps(SERVER_METADATA)),
            "file": server_file_path
        }
        
        response = requests.post(f"https://minecraft.curseforge.com/api/projects/{CF_ID}/upload-file", headers=headers, files=files)
        response_json = response.json()
        
        if "errorCode" in response_json:
            raise Exception(f"Failed to upload server files: {response_json}")
        
        if "id" in response_json:
            print("Uploaded server files!")

# Function to create a new GitHub releaseg
def new_github_release():
    if json_data.get("ENABLE_GITHUB_RELEASE_MODULE") == True:
        print("Making GitHub Release...")
        
        base64_token = base64.b64encode(GITHUB_TOKEN.encode()).decode()
        uri = f"https://api.github.com/repos/{GITHUB_NAME}/{GITHUB_REPOSITORY}/releases?access_token={GITHUB_TOKEN}"
        
        headers = {
            "Authorization": f"Basic {base64_token}"
        }
        
        body = {
            "tag_name": MODPACK_VERSION,
            "name": MODPACK_VERSION,
            "generate_release_notes": True
        }
        
        response = requests.post(uri, headers=headers, json=body)
        
        subprocess.run(["powershell", "-NoProfile", "-Command", "github_changelog_generator"])
        
        print("GitHub Release created!")

# Function to update the modlist
def update_modlist():
    MODLIST_CREATOR_JAR = os.path.join(".ModpackSuite", "ModListCreator-4.1.0-fatjar.jar")
    if json_data.get("ENABLE_MODLIST_CREATOR_MODULE") == True:
        try:
            os.mkdir(".ModpackSuite")
        except:
            pass
        if not os.path.exists(MODLIST_CREATOR_JAR) or json_data.get("ENABLE_ALWAYS_UPDATE_JARS") == True:
            if os.path.exists(MODLIST_CREATOR_JAR):
                os.remove(MODLIST_CREATOR_JAR)
            r = requests.get("https://cdn.naylahanegan.com/ModListCreator-4.1.0-fatjar.jar")
            with open(MODLIST_CREATOR_JAR, "wb") as file:
                file.write(r.content)
        
        print("Generating Modlist...")
        
        try:
            os.remove(json_data.get("MODLIST_PATH"))
        except FileNotFoundError:
            pass
        
        subprocess.run(["java", "-jar", MODLIST_CREATOR_JAR, "modlist", "--output", json_data.get("MODLIST_PATH"), "--detailed", f"{CLIENT_ZIP_NAME}.zip"], check=True)
        
        shutil.copy(json_data.get("MODLIST_PATH"), os.path.join(instance_root, "MODLIST.md"))

if __name__ == "__main__":
    start_location = os.getcwd()
    os.chdir(instance_root)
    
    try:
        test_for_dependencies()
        new_client_files()
        push_client_files()
        
        new_github_release()
        new_changelog()
        update_modlist()
        
        print("Modpack Upload Complete!")
    
    finally:
        os.chdir(start_location)