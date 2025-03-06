run_app:
	# Start the app in background and wait for it to be fully up
	python3 app.py &
	while ! nc -z 127.0.0.1 8050; do   
		sleep 1
	done

	# Download the necessary files
	wget -r http://127.0.0.1:8050/
	wget -r http://127.0.0.1:8050/_dash-layout 
	wget -r http://127.0.0.1:8050/_dash-dependencies

	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-graph.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-highlight.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-markdown.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-datepicker.js

	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dash_table/async-table.js
	wget -r http://127.0.0.1:8050/_dash-component-suites/dash/dash_table/async-highlight.js

	wget -r http://127.0.0.1:8050/_dash-component-suites/plotly/package_data/plotly.min.js

	# Move and process the downloaded files
	mkdir -p pages_files
	mv 127.0.0.1:8050/* pages_files/
	ls -a pages_files

	find pages_files -type f -exec sed -i.bak 's|_dash-component-suites|dash_online/_dash-component-suites|g' {} \;
	find pages_files -type f -exec sed -i.bak 's|_dash-layout|dash_online/_dash-layout.json|g' {} \;
	find pages_files -type f -exec sed -i.bak 's|_dash-dependencies|dash_online/_dash-dependencies.json|g' {} \;
	find pages_files -type f -exec sed -i.bak 's|_reload-hash|dash_online/_reload-hash|g' {} \;
	find pages_files -type f -exec sed -i.bak 's|_dash-update-component|dash_online/_dash-update-component|g' {} \;

	mv pages_files/_dash-layout pages_files/_dash-layout.json
	mv pages_files/_dash-dependencies pages_files/_dash-dependencies.json

	# Terminate the specific app process gracefully
	ps -C python -o pid= | xargs -r kill

clean_dirs:
	ls
	rm -rf 127.0.0.1:8050/
	rm -rf pages_files/
	rm -rf joblib
