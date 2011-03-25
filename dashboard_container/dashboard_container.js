
	GridItem = function(jqo, w, h) {
		this.jqobject = jqo;
		this.colspan = w
		this.rowspan = h
		
		jqo.addClass("grid-item");
		jqo.addClass("ui-widget-content");
		jqo.draggable();
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
		jqobject.append('<div class="grid-columns"></div>')
		for (var n = 0; n < num_cols; n++) {
			jqobject.find('.grid-columns').append('<ul></ul>')
		}
		
		var column_nodes = jqobject.find(".grid-columns > ul")
		var item_nodes = jqobject.find(".grid-items > *")
		
		column_nodes.each(function(index, column_node) {
			column = new GridColumn($(column_node))
			columns.push(column)
		});
		
		item_nodes.each(function(index, item_node) {
			item = new GridItem($(item_node))
			items.push(item)
			
			make_space_for(item, columns)
		});
		
		return { 
			items : items, 
			columns : columns 
		}
	}
	
	function make_space_for(item, columns) {
		/* should determine the top-left most position that the given item can
		 * be placed within the columns.  For now will just use the first 
		 * available space (and assume that all items will be 1x1). */
		
		var column_to_place_in = null;
		for (var c in columns) {
			var current_column = columns[c];
			if (column_to_place_in === null) {
				column_to_place_in = current_column
			}
			else if (
				current_column.cells.length < column_to_place_in.cells.length) {
				column_to_place_in = current_column
			}
		}
		
		var cell = new GridCell($('<li></li>'))
		column_to_place_in.cells.push(cell)
		column_to_place_in.jqobject.append(cell.jqobject)
		cell.jqobject.addClass('empty-cell')
	}

