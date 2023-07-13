# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2022, Input Labs Oy.

BLENDER := 'blender'
# BLENDER := '/Applications/Blender.app/Contents/MacOS/Blender'

default: release

release: clean stl
	mkdir -p release/
	zip -u release/blender.zip blender/*.blend
	zip -u release/stl.zip stl/*.stl stl/**/*.stl

clean:
	rm -rf release/*
	rm -rf stl/*
	mkdir -p stl
	mkdir -p stl/tightness_variants

stl: clean
	$(BLENDER) blender/case_front.blend --background --python scripts/export.py
	$(BLENDER) blender/case_back.blend --background --python scripts/export.py
	$(BLENDER) blender/trigger_R1.blend --background --python scripts/export.py
	$(BLENDER) blender/trigger_R2.blend --background --python scripts/export.py
	$(BLENDER) blender/trigger_R4.blend --background --python scripts/export.py
	$(BLENDER) blender/anchor.blend --background --python scripts/export.py
	$(BLENDER) blender/dhat.blend --background --python scripts/export.py
	$(BLENDER) blender/scrollwheel.blend --background --python scripts/export.py
	$(BLENDER) blender/button_abxy.blend --background --python scripts/export.py
	$(BLENDER) blender/button_dpad.blend --background --python scripts/export.py
	$(BLENDER) blender/button_select.blend --background --python scripts/export.py
	$(BLENDER) blender/thumbstick.blend --background --python scripts/export.py
	$(BLENDER) blender/button_home.blend --background --python scripts/export.py
	$(BLENDER) blender/case_cover.blend --background --python scripts/export.py
	$(BLENDER) blender/hexagon.blend --background --python scripts/export.py
	$(BLENDER) blender/soldering_stand.blend --background --python scripts/export.py
