	
	Grid = function(columns, items) {
		this.columns = columns || []
		this.items = items || []
		
		this.append_item = function(item) {
			/* should determine the top-left most position that the given item can
			 * be placed within the columns.  For now will just use the first 
			 * available space (and assume that all items will be 1x1). */
		
			// Determine which column to place the item in
			var column_to_place_in = null;
			for (var c in columns) {
				var current_column = this.columns[c];
				if (column_to_place_in === null) {
					column_to_place_in = current_column
				}
				else if (
					current_column.cells.length < column_to_place_in.cells.length) {
					column_to_place_in = current_column
				}
			}
			
			// Create cell(s) to place the item
			var cell = new GridCell($('<li></li>'))
			cell.item = item
			column_to_place_in.cells.push(cell)
			column_to_place_in.jqobject.append(cell.jqobject)
		}
		
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
		jqobject.find('.grid-columns').append('<div style="clear: both"></div>')
		
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

