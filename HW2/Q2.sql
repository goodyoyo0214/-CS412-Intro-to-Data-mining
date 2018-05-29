use HW2;
select * from business;

select distinct City, Category, Rating, Price,count(*) from business group by City, Category, Rating, Price;

select distinct state, Category, Rating, Price,count(*) from business group by state, Category, Rating, Price;

select state, Rating, Price, count(*)
	from business 
	where State = 'illinois' and Rating = 3 and Price = 'moderate';
	
    
select city, Category , count(*)
	from business 
	where city = 'chicago' and Category = 'food';
    
