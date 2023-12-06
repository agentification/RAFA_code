

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b a)
(on c e)
(ontable d)
(ontable e)
(on f g)
(on g i)
(on h b)
(on i d)
(clear c)
(clear f)
(clear h)
)
(:goal
(and
(on b g)
(on c f)
(on e i)
(on f a))
)
)


