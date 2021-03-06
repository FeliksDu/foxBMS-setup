﻿# @copyright &copy; 2010 - 2017, Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. All rights reserved.
#
# BSD 3-Clause License
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 1.  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 2.  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3.  Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# We kindly request you to use one or more of the following phrases to refer to foxBMS in your hardware, software, documentation or advertising materials:
#
# &Prime;This product uses parts of foxBMS&reg;&Prime;
#
# &Prime;This product includes parts of foxBMS&reg;&Prime;
#
# &Prime;This product is derived from foxBMS&reg;&Prime;

"""
@file       clean.py
@date       05.05.2017 (date of creation)
@author     foxBMS Team
@ingroup    tools
@prefix     none
@brief      clean wrapper for waf

Helper script for cleaning binaries and documentation of foxBMS
"""

import os
import sys
import subprocess
import argparse
import logging
import shutil

sys.dont_write_bytecode = True

TOOLCHAIN_BASIC_CONFIGURE = sys.executable + ' ' + \
    os.path.join('foxBMS-tools', 'waf-1.9.13') + ' ' + 'configure'

def clean_prcoess(cmd, supress_output=False):
    logging.debug(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, \
        stderr=subprocess.PIPE)
    out, err = proc.communicate()
    rtn_code = proc.returncode

    if supress_output is False:
        if out:
            logging.info(out)
        if err:
            logging.error(err)

    if rtn_code == 0 or rtn_code == None:
        print "Success: Process return code %s" % (str(rtn_code))
    else:
        print "Error: Process return code %s" % (str(rtn_code))
        sys.exit(1)

def clean(mcu_switch=None, supress_output=False):
    cmd = TOOLCHAIN_BASIC_CONFIGURE +  " "
    if mcu_switch is None:
        sphinx_build_dir = os.path.join("build", "sphinx")
        if os.path.isdir(sphinx_build_dir):
            shutil.rmtree(sphinx_build_dir)
        else:
            print "Nothing to clean..."
    elif mcu_switch == "-p" or mcu_switch == "-s":
        cmd += " " + mcu_switch + " " + "clean"
    else:
        print "Invalid clean argument: \"%s\"" % (mcu_switch)
        sys.exit()
    clean_prcoess(cmd, supress_output)

def main(cmd_line_args):
    if cmd_line_args.all:
        clean()
        clean(mcu_switch='-p')
        clean(mcu_switch='-s')
    elif cmd_line_args.sphinx:
        clean()
    elif (cmd_line_args.primary and not cmd_line_args.secondary) or \
        (not cmd_line_args.primary and cmd_line_args.secondary):
            if cmd_line_args.primary:
                mcu_switch = "-p"
            if cmd_line_args.secondary:
                mcu_switch = "-s"
            clean(mcu_switch)
if __name__ == '__main__':
    HELP_TEXT = """This script cleans the software and documentation 
repositories based on the specified commands."""
    parser = argparse.ArgumentParser(description=HELP_TEXT, \
        formatter_class=argparse.RawTextHelpFormatter, add_help=True)
    opt_args = parser.add_argument_group('optional arguments:')
    opt_args.add_argument('-sphi', '--sphinx', action='store_true', \
        required=False, help='cleans sphinx documenation')
    opt_args.add_argument('-p', '--primary', action='store_true', \
        required=False, help='cleans primary binaries and documentation')
    opt_args.add_argument('-s', '--secondary', action='store_true', \
        required=False, help='cleans secondary binaries and documentation')
    opt_args.add_argument('-dox', '--doxygen', action='store_true', \
        required=False, help='cleans the software documentation for the specified mcu (-p, -s)')
    opt_args.add_argument('-a', '--all', action='store_true', \
        required=False, help='cleans all of the above mentioned')
    CMD_LINE_ARGS = parser.parse_args()

    main(CMD_LINE_ARGS)
