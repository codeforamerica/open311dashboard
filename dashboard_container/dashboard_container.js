
	
	Grid = function(columns, items) {
		this.columns = columns || []
		this.items = items || []
		
		/**
		 * Grab the column in the grid that has the lowest-most cell.
		 * @return {GridColumn} The column with the lowest-most cell.
		 */
		this.get_lowest_column = function() {
			// _last_lowest_column is used for the get_next_lowest_column() 
			// method.  If it's null, then get_next_lowest_column() will return
			// the lowest column.
			this._last_lowest_column = null
			
			lowest_column = this.get_next_lowest_column()
			
			return lowest_column
		}
		
		/**
		 * Grab the column in the grid that has the next lowest-most cell.  If 
		 * get_lowest_column hasn't been called, this will grab the column with
		 * the lowest-most cell.
		 * @return {GridColumn} The column with the next lowest-most cell.
		 */
		this.get_next_lowest_column = function () {
			var next_lowest_column = null;
			
			for (var c in columns) {
				var current_column = this.columns[c]
				
				// Exclude if the current_column is lower or equal to the
				// _last_lowest_column.  If get_lowest_column() hasn't been
				// calld, then _last_lowest_column will not be set.
				if (this._last_lowest_column) {
					if (current_column === this._last_lowest_column ||
						current_column.cells.length < this._last_lowest_column.cells.length ||
						(current_column.cells.length == this._last_lowest_column.cells.length &&
						 $.inArray(current_column.jqobject, this._last_lowest_column.jqobject.nextAll())))
						continue
				}
				
				if (next_lowest_column === null) {
					next_lowest_column = current_column
				}
				else if (current_column.cells.length < 
				         next_lowest_column.cells.length) {
					next_lowest_column = current_column
				}
			}
			
			this._last_lowest_column = next_lowest_column
			return next_lowest_column
		}
		
		/**
		 * Add the item to the end of the column with the specified index.  If
		 * no index is given, then the item will be placed in the first position
		 * where it fits, searching across the columns left-to-right, then down 
		 * the rows.
		 */
		this.append_item = function(item, column_index) {
			// Determine which column to place the item in
			var column_to_place_in
			if (column_index !== undefined) {
				column_to_place_in = this.columns[column_index]
			}
			else {
				column_to_place_in = this.get_lowest_column()
			}
			
			// Create cell(s) to place the item.  The item may span more than
			// one row and/or column, so enough cells need to be created to 
			// accommodate the item, whatever the size.
			var curr_column = column_to_place_in
			for (var c = 0; c < item.colspan; c++) {
				for (var r = 0; r < item.rowspan; r++) {
					var cell = new GridCell($('<li></li>'))
					cell.item = item
					curr_column.cells.push(cell)
					curr_column.jqobject.append(cell.jqobject)
				}
				curr_column = this.get_column_after(curr_column)
			}
		}
		
		/**
		 * Get the column after (to the right) the given column.
		 * @return {GridColumn} The column after the given one
		 */
		this.get_column_after = function(column) {
			var next_column
			var next_jqo = column.jqobject.next()
			
			for (c in this.columns) {
				var column = this.columns[c]
				if (column.jqobject[0] === next_jqo[0]) {
					next_column = column
					break
				}
			}
			return next_column
		}
		
		/**
		 * Update the offsets of the grid items based on the cells that each
		 * occupies.
		 */
		this.update_positions = function() {
			for (var i in this.columns) {
				var column = columns[i]
				for (var j in column.cells) {
					var cell = column.cells[j]
					
					var item = cell.item
					if (item) {
						item.jqobject.offset(cell.jqobject.offset())
					}
				}
			}
		}
	}
	
	GridItem = function(jqo, w, h) {
		this.jqobject = jqo;
		
		if (w === undefined) w = 1
		if (h === undefined) h = 1
		
		this.colspan = w
		this.rowspan = h
		
		jqo.addClass("grid-item");
		jqo.addClass("ui-widget-content");
		jqo.draggable({
			start : function (event, ui) {
				var x = event.clientX
				var y = event.clientY
				
				
			}
		});
		
	}
	
	GridColumn = function(jqo, index) {
		this.jqobject = jqo
		this.colindex = index
		this.cells = []
		
		jqo.addClass("grid-column");
	}
	
	GridCell = function(jqo, index) {
		this.jqobject = jqo
		
		jqo.addClass("grid-cell");
	}
	
	function prepare_grid(jqobject, num_cols) {
		var items = []
		var columns = []
		
		// alter the dom
		jqobject.children().wrapAll('<div class="grid-items"></div>')
		jqobject.prepend('<div class="grid-columns"></div>')
		for (var n = 0; n < num_cols; n++) {
			jqobject.find('.grid-columns').append('<ul></ul>')
		}
		
		var column_nodes = jqobject.find(".grid-columns > ul")
		var item_nodes = jqobject.find(".grid-items > *")
		
		column_nodes.each(function(index, column_node) {
			column = new GridColumn($(column_node))
			columns.push(column)
		});
		
		var grid = new Grid(columns)
		
		item_nodes.each(function(index, item_node) {
			item = new GridItem($(item_node))
			items.push(item)
			
			grid.append_item(item)
		});
		
		grid.update_positions()
		
		return grid
	}

