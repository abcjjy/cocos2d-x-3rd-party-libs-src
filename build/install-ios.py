#!/usr/bin/env python

import argparse
import shutil
import os.path
import os

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--src', default=os.path.join(os.path.dirname(__file__), 'ios'))
ap.add_argument('-d', '--dest', default=os.path.join(os.path.dirname(__file__), '../../libcocos2dx/external'))

args = ap.parse_args()

assert(os.path.exists(args.src) and os.path.exists(args.dest))

cps = {
        "png":'png',
        "z":'zlib',
        "lua":'lua/lua',
        "luajit":'lua/luajit',
        "websockets":'websockets',
        "curl":'curl',
        "freetype":'freetype2',
        "jpeg":'jpeg',
        "tiff":'tiff',
        "webp":'webp',
        "chipmunk":'chipmunk',
        "ssl":'openssl',
        # "rapidjson":'rapidjson',
        "bullet":'bullet',
        "box2d":'Box2D',
        'crypto': 'openssl'
        }

xpinclude = set(['curl', 'freetype', 'jpeg', 'ssl', 'png', 'spidermonkey', 'tiff', 'webp', 'websockets'])
hspecials = {
        'webp': ('include/webp', 'include/ios'),
        'lua': None,
        'websockets': ('include/libwebsockets.h', 'include/ios/libwebsockets.h'),
        'crypto': None,
        }

def onerror():
    print 'error'

for slib, dlib in cps.iteritems():
    dst = os.path.join(args.dest, dlib)
    src = os.path.join(args.src, slib)

    os.system('cp -p {}/*.a {}'.format(os.path.join(src, 'prebuilt'), os.path.join(dst, 'prebuilt/ios')))
    
    if slib not in hspecials:
        dstinclude = os.path.join(dst, 'include')
        if slib in xpinclude:
            dstinclude = os.path.join(dst, 'include/ios')
        shutil.rmtree(dstinclude, ignore_errors=True, onerror=onerror)
        shutil.copytree(os.path.join(src, 'include'), dstinclude)
    elif hspecials[slib]:
        isrc, idst = hspecials[slib] 
        srcinclude = os.path.join(src, isrc)
        dstinclude = os.path.join(dst, idst)
        if os.path.isdir(srcinclude):
            shutil.rmtree(dstinclude, ignore_errors=True, onerror=onerror)
            shutil.copytree(srcinclude, dstinclude)
        else:
            shutil.copy(srcinclude, dstinclude)

