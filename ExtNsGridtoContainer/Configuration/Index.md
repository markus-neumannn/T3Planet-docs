---
title: "Configuration"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_GridtoContainer"
  - "Configuration"
sidebarTitle: "Configuration"
---

# Configuration

## Preconditions for Migration:

We assume you have EXT:grid elements and EXT:container Extension.For migration you must set Container Configuration same as Grid Configuration !

When you make the container configuration then some points are strict to follow for migration process
**Container CType** and Old Gridelements **tx_gridelements_backend_layout** the key must be the same.

**For Example :** I need to migrate the Grid of **"nsBase1Col"** then while in container configuration, you need to put container's CType as **"nsBase1Col"**

### Grid Backend Layout Key

![Grid Backend Layout Key](./images/Grid_Backend_Layout_Key.jpg)

### Container CType

![Container CType](./images/containerCtype.webp)

**For colPos > Grid colPos:** For example, the Grid's Colpos is '1' then while in container configuration you need to put colPos higher than Grid. like '101'
Because In migration process, we make the same container's colpos with which comes of grid's colPos for the placing Content Elements of Grid in Container while migrating.
Like. Grid ColPos\*\* '1'[tx_gridelements_columns] and in container configuration, colPos is '101'\*\*

Then in migrating process, we make same colPos for placing Content Elements \$colPos = \$element['tx_gridelements_columns'] + 100;"

![Grid_colposs](./images/Grid_colpos.jpg)

While container colPos must be different like
![Container_colpos](./images/Container_colpos.webp)

## We provide 2 options for migrating grids

**Option 1:Migration of all Grids available on the site.**
![Migration](./images/Migration.Jpg)

**Option 2:If you have a small number of grids then you can use the second option "Migration from grid elements layout key"**
![All_grid_layout](./images/All_grid_layout.webp)

## Migration Process:

**Grid:** For example You want to migrat this gird
![grid](./images/grid.jpg)

**Follow this Steps>>**

**Step 1:** Enter container CType with same as Grid Backend Layout Key
![Grid_Backend_Layout_Key](./images/Grid_Backend_Layout_Key.jpg)

**Step 2:** Click on "Migrate Button" It will show message like "Successfully migrated"
![Success_msg](./images/Success_msg.jpg)

**Step 3:** Now, check the migration!
![Migration_Done](./images/Migration_Done.Jpg)

**This Extension also Provide feature to migrate Hidden content Elements!**
![hidden_1](./images/hidden_1.jpg)

![Hidden_2](./images/hidden_2.jpg)

**That's it, Now you can enjoy all the benifits of this extension :)**
