# -----------------------------------
# Import
# -----------------------------------
import json, re, sys, argparse, shutil
from pathlib import Path
from importlib.metadata import version
from datetime import datetime

import loadskernelutils

# -----------------------------------
# Collor codes
# -----------------------------------
RED    = '\033[31m'
GREEN  = '\033[32m'
YELLOW = '\033[33m'
BLUE   = '\033[34m'
RESET  = '\033[0m'

# -----------------------------------
# Arguments
# -----------------------------------
# Parser
parser = argparse.ArgumentParser(
            prog='LKU-script',
            description='Patches code changes to existing source code',
            epilog='Help menu of LKU-script')
# Arguments
parser.add_argument(
    "--module_path",
    type=str,
    required=False,
    default=None,
    help="Path pointing to the module of where the source code that should be patched is located."
)
parser.add_argument(
    "--export",
    action="store_true",
    default=False,
    help="Enables the export of the final report to the module's path."
)
# Parse arguments
args = parser.parse_args()

def patcher_info():
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%d.%m.%Y")
    module_name = "loadskernelutils"
    module_version = version(module_name)

    print(r" _      _  __   ____          _          _                  ")
    print(r"| |    | |/ /  |  _ \   __ _ | |_   ___ | |__    ___  _ __  ")
    print(r"| |    | ' /   | |_) | / _` || __| / __|| '_ \  / _ \| '__| ")
    print(r"| |___ | . \   |  __/ | (_| || |_ | (__ | | | ||  __/| |    ")
    print(r"|_____||_|\_\  |_|     \__,_| \__| \___||_| |_| \___||_|    ")
    print(f"                                                            ")
    print(f"                    Version {module_version}                ")
    print(f"          Started on {current_date} at {current_time}       ")
    print(f"                                                            ")

# -----------------------------------
# Main
# -----------------------------------
def main(module_path: Path = None, export: bool = None):
    """Patches changes to LoadsKernel source code

    Args:
        module_path (Path): Path pointing to a python module's source code
        export (bool): Enables the export of the final report to the module's path

    Returns:
        None

    Internal variables:
        target (Path): LoadsKernel repository path.
        e (Exception): Any error raised while checking the path.
        patches_file (Path): Json file containing patch information.
        module (Path): Module path containing the new source code and patch codes.
        patches_json (str): Patches intermediate string.
        patches (list): Patches list.
        p (dict): Current Patch dictionary.
        patch_file (Path): Path of the patch file containing the new code.
        patch_lines (str): New code.
        target_file (Path): Path of the target file.
        target_lines (list): Row by row representation of the target file.
        matches (list): List containing all found anchors.
        ...

    Raises:
        SystemExit: If the path does not exist or cannot be checked.
    """

    # -----------------------------------
    # Get user input
    # -----------------------------------
    if module_path == None:
        print('Please specify a local LoadsKernel repository path:')
        print('The path must point exactly on the main folder of the source code!')
        print('eg. (..\\LoadsKernel\\loadskernel)')

        target = Path(input('LoadsKernel path: '))
    else:
        target = Path(module_path)
        print(f'The local LoadsKernel repository is located at: {target}')

    # Test the target if it is a path or not
    try: 
        if not Path(target).exists():
            print ('Your specified path does not exist.')
            sys.exit(1)
    except Exception as e:
        print (f'There was an error with your specified path. The LoadsKernelPatcher will end. Error: {e}')
        sys.exit(1)

    print('The LoadsKernel\'s source code will now be patched ...')

    # -----------------------------------
    # Reading patch data
    # -----------------------------------
    patches_root_file = loadskernelutils.get_patches()
    module = loadskernelutils.get_package_dir()

    with open(patches_root_file, 'r', encoding='utf-8') as f:
        patches_root_json = f.read()
    patch_files = json.loads(patches_root_json)
    # Read patches
    patches = []
    for pf in patch_files['patches']:
        with open(loadskernelutils.get_patch_file(pf), 'r', encoding='utf-8') as f:
            local_patches = json.loads(f.read())
            for p in local_patches['patches']:
                patches.append(p)

    # -----------------------------------
    # Patching
    # -----------------------------------
    performed_patches = []
    patch_id = 1
    # dict = {'id':0 name':'patch_name', 'success':True, 'target_file':"target_file", 'start_line':0, 'end_line':1, 'info':'info'}
    for p in patches:
        # Start patch process
        if 'patch_name' in p:
            print(f"Start patching \"{p["patch_name"]}\"")
            info = None

            # -----------------------------------
            # Uploading
            # -----------------------------------
            if p['patch_type'] == 'add_file':
                target_directory = target / p['target_dir']
                upload_file = module / p['upload_file']
                target_file = target_directory / upload_file.name
                shutil.copy(upload_file, target_directory)
                info = 'File upload!'

                # Create report entry
                performed_patches.append({'id': f'{patch_id}', 'name':p['patch_name'], 'success':True, 'target_file':target_file, 'start_line':'/', 'end_line':'/', 'info':info})
                
            # -----------------------------------
            # Adding sections to source file
            # -----------------------------------
            else:
                # Patch code into sorce file
            
                # Reading target file
                target_file = target / p['target_file']
                target_lines = target_file.read_text().splitlines(keepends=True)

                # Selecting anchor search mechanism
                if 'anchor_type' in p:
                    match p['anchor_type']:
                        case 'function':
                            # -----------------------------------
                            # Function anchor
                            # -----------------------------------
                            # Find the anchor line
                            matches = [i for i, l in enumerate(target_lines) if re.search(f'def {p['anchor']}', l)]
                            #
                            # Checking mechanis of _ after function name.
                            #
                        
                        case 'loop':
                            # -----------------------------------
                            # Loop anchor
                            # -----------------------------------
                            matches = [
                                i for i, line in enumerate(target_lines)
                                if re.search(re.escape(f"{p['loop_type']} {p['anchor']}") + r'\s*$', line)
                            ]

                        case 'line':
                            # -----------------------------------
                            # Line anchor
                            # -----------------------------------
                            # Find the anchor line
                            matches = [i for i, line in enumerate(target_lines) if line.strip() == p['anchor']]

                            if not matches:
                                print(f"The \'anchor\':\'{p['anchor']}\' declarated in {p["patch_name"]} was not found in {p['target_file']}. A patch can therefore not be performed!")
                                performed_patches.append({'id': patch_id, 'name':p['patch_name'], 'success':False, 'target_file':None, 'start_line':None, 'end_line':None, 'info':'Patch anchor not exisiting!'})
                                patch_id += 1
                                continue

                        case _:
                            print(f" The \'anchor_type\':\'{p["anchor_type"]}\' declarated in {p["patch_name"]} is not supported. A patch can therefore not be performed!")
                            performed_patches.append({'id': patch_id, 'name':p['patch_name'], 'success':False, 'target_file':None, 'start_line':None, 'end_line':None, 'info':'Patch type not exisiting!'})
                            patch_id += 1
                            continue
                else:
                    print(f" No \'anchor_type\' has been declared for {p["patch_name"]}. A patch can therefore not be performed!")
                    performed_patches.append({'id': patch_id, 'name':p['patch_name'], 'success':False, 'target_file':None, 'start_line':None, 'end_line':None, 'info':'No patch type decleraded!'})
                    patch_id += 1
                    continue

                # -----------------------------------
                # Performe patching
                # -----------------------------------
                # flush counter for the correct row numbering in the patch report
                line_start_flush = 0
                line_end_flush = 0
                anchor_ids = p['anchor_ids']
                # -----------------------------------
                # Match loop
                # -----------------------------------
                for i, m in enumerate(matches):
                    if anchor_ids == 'all' or i + 1 in anchor_ids:
                        # Current anchor position
                        idx = matches[i]
                        # Update target lines (required for multi patches)
                        target_lines = target_file.read_text().splitlines(keepends=True)
                        # -----------------------------------
                        # Patch type loop
                        # -----------------------------------
                        match p['patch_type']:
                            case 'add':
                                # Reading patch file
                                patch_file = module / p['patch_file']
                                patch_lines = Path(patch_file).read_text()
                                # Get anchor shift (required for auto shift)
                                num_spaces = len(target_lines[idx]) - len(target_lines[idx].lstrip())
                                # Set auto shift or fix shift size
                                # Slide-in (required for python syntax)
                                if p["shift"] == "auto":
                                    spaces = " " * num_spaces
                                else:
                                    spaces = " " * p["shift"]
                                # add an emtpy row befor and after the patch
                                if 'patch_with_distance' not in p or p['patch_with_distance'] == True:
                                    indented = (
                                        ["\n"]
                                        + [
                                        (spaces + line if line.strip() else line) + "\n"
                                        for line in patch_lines.splitlines()
                                        ]
                                        + [ "\n"]
                                    ) 
                                    line_start_flush = 1
                                    line_end_flush = 2
                                else:
                                    indented = (
                                        [
                                        (spaces + line if line.strip() else line) + "\n"
                                        for line in patch_lines.splitlines()
                                        ]
                                    )
                                # Determining correct anchor position for patch, before or after the anchor
                                if p['where'] == 'before':
                                    # Check if comment on top of the anchor:
                                    while idx > 0:
                                        if not target_lines[idx - 1].lstrip().startswith("#"): 
                                            break
                                        idx -= 1
                                elif p['where'] == 'after':
                                    if p['anchor_type'] == 'function' or p['anchor_type'] == "loop":
                                        # Search for end of function (-1 required since it checks the next line not the current one)
                                        while idx < len(target_lines) - 1:
                                            idx += 1
                                            line = target_lines[idx]
                                            # only spaces (or empty)
                                            if line.strip() == '': continue
                                            # number of leading spaces
                                            indent = len(line) - len(line.lstrip(' '))
                                            # fewer spaces
                                            if indent <= num_spaces: break
                                    elif p['anchor_type'] == 'line':
                                        # Go to next row
                                        idx += 1

                                # Write patche
                                target_lines[idx:idx] = indented
                                target_file.write_text("".join(target_lines))

                                # After add patch, update numbering of found matches
                                # such that the new row numbering matches
                                for j in enumerate(matches):
                                    matches[j[0]] = matches[j[0]] + len(indented)

                            case 'comment':
                                line = target_lines[idx]
                                indent = len(line) - len(line.lstrip())

                                # Write patche
                                target_lines[idx] = line[:indent] + '# ' + line[indent:]
                                target_file.write_text("".join(target_lines))

                            case 'delete':
                                print('delete patch type')
                                
                            case _:
                                print(f'Patch type can not be found')

                        # Create report entry
                        start_line = idx + line_start_flush
                        end_line = idx + len(patch_lines.splitlines()) + line_end_flush
                        performed_patches.append({'id': f'{patch_id}.{i + 1}', 'name':p['patch_name'], 'success':True, 'target_file':target_file, 'start_line':start_line, 'end_line':end_line, 'info':info})
            # Next patch
            patch_id += 1
        
    # -----------------------------------
    # Patch report
    # -----------------------------------
    # Print report
    print(f'{BLUE}==================== REPORT ===================={RESET}')
    for p in performed_patches:
        color = GREEN if p['success'] else RED
        status = 'successfully' if p['success'] else 'unsuccessfully'
        lines = f'Patch starts at line: {YELLOW}{p['start_line']}{RESET} and ends at line: {YELLOW}{p['end_line']}{RESET} in file {YELLOW}{p['target_file']}{RESET}.' if p['success'] else ''
        info = f'{BLUE}{p['info']}{RESET}' if p['info'] != None else ''

        print(f"{BLUE}{p['id']}:{RESET} \'{p['name']}\' was {color}{status}{RESET} patched! {lines} {info}")
    # Export report
    if export == True:
        current_time = datetime.now().strftime("%H%M%S")
        current_date = datetime.now().strftime("%d%m%Y")
        report = module_path / Path(f'patch_report_{current_date}_{current_time}.text')
        # Write report
        with open(report, "w", encoding="utf-8") as file:
            for p in performed_patches:
                status = 'successfully' if p['success'] else 'unsuccessfully'
                lines = f'Patch starts at line: {p['start_line']} and ends at line: {p['end_line']} in file {p['target_file']}.' if p['success'] else ''
                info = f'{p['info']}' if p['info'] != None else ''
                file.write(f"{p['id']}: \'{p['name']}\' was {status} patched! {lines} {info}\n")
        print(f'Reprot exported to: {report}')

# -----------------------------------
# Entry point for manuel execution
# -----------------------------------
if __name__ == '__main__':
    patcher_info()
    main()

# -----------------------------------
# Entry point for terminal execution
# -----------------------------------
def patcher_terminal():
    # Print the patcher logo
    patcher_info()
    # 
    if args.module_path == None:
        parser.print_help()
        print()
        print('Please specify a module Path on which the patches should be applied.')
        print('Therefor write \' LKU-setup --module_path ../*individual_path*/LoadsKernel \' in the command line.')
    else:
        # Check if the parsed argument is a path
        try:
            if not Path(args.module_path).exists:
                print(f'The path: {args.module_path} does not exist.')
                sys.exit(1)
        except Exception as e:
            print(f'An Error occoured during the path check of \'{args.module_path}\'. {e}.')
            sys.exit(1)
        # Start the main patcher logic
        main(module_path= args.module_path, export= args.export)