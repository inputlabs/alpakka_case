# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2022, Input Labs Oy.

BLENDER := 'blender'
# BLENDER := '/Applications/Blender.app/Contents/MacOS/Blender'

default: release

release: stl
	mkdir -p release/
	zip -u release/blender.zip blender/*.blend
	zip -u release/stl.zip stl/*.stl stl/**/*.stl
	zip -u release/step.zip step/*.step stl/**/*.step

clean:
	rm -rf release/*
	rm -rf stl/*
	rm -rf step/*
	mkdir -p stl
	mkdir -p step

stl: clean blend b123d

blend:
	$(BLENDER) blender/case_front.blend --background --python scripts/export_blender.py
	$(BLENDER) blender/case_back.blend --background --python scripts/export_blender.py
	$(BLENDER) blender/trigger_R2.blend --background --python scripts/export_blender.py
	$(BLENDER) blender/trigger_R4.blend --background --python scripts/export_blender.py
	$(BLENDER) blender/dhat.blend --background --python scripts/export_blender.py
	$(BLENDER) blender/thumbstick.blend --background --python scripts/export_blender.py
	$(BLENDER) blender/button_home.blend --background --python scripts/export_blender.py
	$(BLENDER) blender/hexagon.blend --background --python scripts/export_blender.py
	$(BLENDER) blender/soldering_stand.blend --background --python scripts/export_blender.py

b123d:
	python3 scripts/export_b123d.py
