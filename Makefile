default: release

release: clean stls
	sh -e scripts/release.sh

clean:
	rm -rf release/*
	rm -rf STL/*

stls: clean
	blender blender/case_front.blend --background --python scripts/export.py
	blender blender/case_back.blend --background --python scripts/export-z.py
	blender blender/trigger_R1.blend --background --python scripts/export.py
	blender blender/trigger_R2.blend --background --python scripts/export-z.py
	blender blender/trigger_R4.blend --background --python scripts/export-yz.py
	blender blender/anchor.blend --background --python scripts/export-z.py
	blender blender/dhat.blend --background --python scripts/export.py
	blender blender/scrollwheel.blend --background --python scripts/exportwheelsupport.py
	blender blender/button_abxy.blend --background --python scripts/export.py
	blender blender/button_dpad.blend --background --python scripts/export.py
	blender blender/scrollwheel.blend --background --python scripts/exportwheelshaft.py
	blender blender/button_select.blend --background --python scripts/export.py
	blender blender/thumbstick.blend --background --python scripts/export.py
	blender blender/button_home.blend --background --python scripts/exporthome.py
	blender blender/case_cover.blend --background --python scripts/export.py
	blender blender/scrollwheel.blend --background --python scripts/exportwheel.py
	blender blender/hexagon.blend --background --python scripts/export-z.py
	blender blender/soldering_stand.blend --background --python scripts/exportstand.py
