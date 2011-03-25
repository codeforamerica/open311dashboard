
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
		
		jqo.addClass("grid-column");
	}
	
	function prepare_grid(jqobject) {
		var items = []
		var columns = []
		
		var column_nodes = jqobject.find(".grid-columns > ul")
		var item_nodes = jqobject.find(".grid-items > *")
		
		column_nodes.each(function(index, column_node) {
			column = new GridColumn($(column_node))
			columns.push(column, index)
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
		
		var cell_to_place = null;
		for (var c in columns) {
			column = columns[c];
			var current_cell = column.get_lowest_cell()
			if (!cell_to_place) {
				cell_to_place = current_cell
			}
			else if (current_cell && 
			    current_cell.is_higher_than(cell_to_place)) {
				cell_to_place = current_cell
			}
		}
	}

